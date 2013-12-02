
import decimal
from decimal import Decimal as D
import logging
from datetime import date, datetime, timedelta
from decimal import Decimal
import calendar
import six
from billometer.conf import BILLING_CONFIG, EXTRA_RESOURCES
from billometer.utils.graphite import get_resource_data
from billometer.utils.nova_flavor import get_flavor
from billometer.utils.statsd_client import meter
from celery.execute import send_task
from django.conf import settings
from django.db import models
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields.json import JSONField

LOG = logging.getLogger(__name__)

RATE_KIND_CHOICES = (
    ('user', u'user',),
    ('tenant', u'tenant',),
)

RATE_CURRENCY_CHOICES = (
    ('czk', u'CZK',),
    ('eur', u'EUR',),
    ('usd', u'USD',),
)

RESOURCE_TYPE_CHOICES = (
    ('nova.cpu', u'Nova CPU',),
    ('nova.memory', u'Nova memory',),
    ('nova.instance', u'Nova instance',),
    ('cinder.volume', u'Cinder volume',),
    ('glance.image', u'Glance image',),
    ('glance.snapshot', u'Glance snapshot',),
    ('neutron.floating_ip', u'Neutron floating IP',),
    ('neutron.network', u'Neutron network',),
    ('neutron.router', u'Neutron router',),
    ('network.rx', u'Network RX',),
    ('network.tx', u'Network TX',),
    #    ('swift.storage', u'Swift storage',),
)


def _get_month_range(now=None):
    today = now or date.today()
    start = date(today.year, today.month, 1)
    month_days = calendar.monthrange(today.year, today.month)[1]
    end = start + timedelta(days=month_days)
    return start, end


class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'), blank=True)
    openstack_tenant = models.CharField(
        max_length=255, verbose_name=_('openstack tenant uid'), blank=True, null=True)
    customer_name = models.CharField(
        max_length=255, verbose_name=_('customer name'), blank=True, null=True)
    customer_id = models.CharField(
        max_length=255, verbose_name=_('customer id'), blank=True, null=True)
    extra = JSONField(verbose_name=_('extra'), null=True, blank=True)

    def sync_quotas(self):
        extra = self.extra.copy()
        extra.update(get_quotas)
        extra.update(cinder.get_quotas)
        self.extra = extra
        self.save()

    def get_resource_price(self, resource, start, end):
        """
        Returns price for given resource type's resources withing time range
        """
        price = 0

        for resource in self.resourcetype_set.filter(resource=resource):
            price += resource.get_instances_price(start, end)

        return price

    def get_resource_prices(self, start_date, end_date):
        return {
            'instances': self.get_resource_price('nova.instance', start_date, end_date),
            'volumes': self.get_resource_price('cinder.volume', start_date, end_date),
            'addresses': self.get_resource_price('neutron.floating_ip', start_date, end_date),
            'images': self.get_resource_price('glance.image', start_date, end_date),
        }

    def get_instance_unit_hours(self, start, end):
        """
        Returns unit hours (more for volumes) for given resource withing time range
        """
        hours = {
            'cpu': 0,
            'memory': 0,
        }
        for resource in self.resourcetype_set.filter(resource='nova.instance'):
            for instance in resource.resourceinstance_set.all():
                hours[
                    'cpu'] += instance.unit_hours_for_period(start, end) * instance.resource_type.extra.get('cpu', 1)
                hours[
                    'memory'] += instance.unit_hours_for_period(start, end) * instance.resource_type.extra.get('memory', 1)

        return hours

    def get_resource_unit_hours(self, resource, name=None, start=None, end=None):
        '''returns collected values for specific resource and date interval'''
        hours = 0

        if name is None:
            resources = self.resourcetype_set.filter(resource=resource)
        else:
            resources = self.resourcetype_set.filter(resource=resource, name=name)

        for resource in resources:
            for instance in resource.resourceinstance_set.all():
                hours += instance.unit_hours_for_period(start, end)

        return hours

    def get_quota(self, resource, name=None):
        if resource == 'nova.cpu':
            return self.extra.get('cpu', 0)
        elif resource == 'nova.memory':
            return self.extra.get('memory', 0)
        elif resource == 'cinder.volume':
            return self.extra.get('disk_%s' % name, 0)
        return 0

    def get_rate(self, resource, name=None):
        default_price = Decimal(0)
        if name is None:
            try:
                r_price = self.resourcetype_set.get(resource=resource).default_price
            except Exception as e:
                try:
                    r_price = self.resourcetype_set.get(
                        resource=resource, openstack_id=self.openstack_tenant).default_price
                except Exception as e:
                    LOG.warning('%s - %s ' % (str(e), resource))
                    r_price = None
            if r_price:
                return r_price
        else:
            try:
                default_price = self.resourcetype_set.get(
                    resource=resource, name=name).default_price
            except Exception as e:
                LOG.warning('%s - %s - %s ' % (str(e), resource, name))
        return default_price

    def get_resource_data(self, resource, start, end):
        value = price = 0
        for resource in self.resourcetype_set.filter(resource=resource):
            _value, _price = resource.totals_for_period(start, end)
            value += _value
            price += _price
        return value, price

    def get_allocation_price(self, resource, name=None, today=None):

        quota = self.get_quota(resource, name)

        if quota == -1:
            return 0

        if today is None:
            today = date.today()

        rate = self.get_rate(resource, name)
        #month_range = calendar.monthrange(today.year, today.month)[1]
        # for variable month days/hours
        #price = decimal.Decimal('0.24') * rate * decimal.Decimal(quota) * decimal.Decimal(month_range)
        # for fixed month days/hours: 730
        price = D('73.0') * rate * decimal.Decimal(quota)

        return price

    def get_quotas_list(self, date=None):
        quotas = SortedDict({
            "name": self.name,
            "uuid": self.openstack_tenant,
            "customer_name": self.customer_name,
            "customer_id": self.customer_id,
            "cpu": self.extra.get("cpu"),
            "cpu_price": self.get_allocation_price("nova.cpu"),
            "memory": self.extra.get("memory"),
            "memory_price": self.get_allocation_price("nova.memory"),
        })
        for r_name, resource in six.iteritems(EXTRA_RESOURCES):
            extra = self.extra.get(r_name)
            if extra:
                quotas[r_name] = extra
                quotas[
                    r_name + "_price"] = self.get_allocation_price(resource["resource"], resource.get("name", r_name))
        return quotas

    def get_overview(self, start, end):
        total_price = 0
        allocation_price = 0
        data = []

        instance_data = self.get_instance_unit_hours(start, end)

        cpu_value = instance_data['cpu']
        cpu_rate = self.get_rate('nova.cpu')
        cpu_price = cpu_value * cpu_rate

        data.append({
            'name': _('VCPU'),
            'value': cpu_value,
            'rate': cpu_rate,
            'price': cpu_price,
        })

        memory_value = instance_data['memory']
        memory_rate = self.get_rate('nova.memory')
        memory_price = memory_value * memory_rate

        data.append({
            'name': _('RAM'),
            'value': memory_value,
            'rate': memory_rate,
            'price': memory_price,
        })

        image_value = self.get_resource_unit_hours('glance.image', None, start, end)
        image_rate = self.get_rate('glance.image', None)
        image_price = image_value * image_rate

        data.append({
            'name': _('Images'),
            'value': image_value,
            'rate': image_rate,
            'price': image_price,
        })

        for r_name, resource in six.iteritems(EXTRA_RESOURCES):
            if resource.get("name", r_name):
                _rate = self.get_rate(resource["resource"], resource.get("name", None))
                _value, _price = self.get_resource_data(resource["resource"], start, end)
                allocation_price += self.get_allocation_price(resource["resource"], resource.get("name", None))
                total_price += _price
                data.append({
                    'name': _(resource.get("label", r_name).capitalize()),
                    'value': _value,
                    'rate': _rate,
                    'price': _price,
                })

        total_price = cpu_price + memory_price + image_price

        if BILLING_CONFIG.get("allocation", True):
            allocation_price += self.get_allocation_price("nova.cpu", None) + \
                self.get_allocation_price("nova.memory", None)

            data.append({
                'name': _('Resource Allocation'),
                'value': None,
                'rate': None,
                'price': allocation_price,
            })
            total_price += allocation_price

        data.append({
            'name': _('Price Total'),
            'value': None,
            'rate': None,
            'price': total_price,
        })

        return data

    def __unicode__(self):

        return self.name

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")


def sync_prices(project):
    """sync all prices in the tenant
       please use sync_price task in tasks.py
       depricated
    """
    query_set = ResourceType.objects \
                            .filter(project=project,
                                    resource="nova.instance")

    for resource_type in query_set.all():

        resource_type.sync_price()


class ResourceType(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'), blank=True)
    project = models.ForeignKey('Project', verbose_name=_('project'))
    resource = models.CharField(max_length=255, verbose_name=_(
        'type'), choices=RESOURCE_TYPE_CHOICES, default='nova.instance')
    openstack_id = models.CharField(
        max_length=255, verbose_name=_('openstack id'), blank=True, null=True)
    ceilometer_query = models.TextField(
        verbose_name=_('id'), editable=False, blank=True, null=True)
    default_price = models.DecimalField(
        u"price", max_digits=18, decimal_places=6, default='1')
    default_threshold = models.DecimalField(
        u"threshold", max_digits=18, decimal_places=3, default='0')
    extra = JSONField(verbose_name=_('extra'), null=True, blank=True)

    def get_data(self, start, end):
        # query celimeter api
        return 5

    def get_network_data(self, start, end):
        '''return network data as tuple tx, rx'''
        tx = self.project.get_resource_unit_hours('network.tx', start=start, end=end)
        rx = self.project.get_resource_unit_hours('network.rx', start, end)
        return tx, rx

    def get_instances_price(self, start, end):
        price = 0
        for instance in self.resourceinstance_set.all():
            # return tuple (value, price)
            price += instance.totals_for_period(start, end)[1]
        return price

    def totals_for_period(self, start, end):
        price = value = 0
        for instance in self.resourceinstance_set.all():
            # return tuple (value, price)
            _value, _price = instance.totals_for_period(start, end)
            price += _price
            value += _value
        return value, price

    @property
    def cpu_price(self):
        try:
            resource_type = ResourceType.objects \
                .get(project=self.project,
                     resource='nova.cpu')
        except Exception as e:
            return 1

        return resource_type.default_price

    @property
    def memory_price(self):
        try:
            resource_type = ResourceType.objects \
                .get(project=self.project,
                     resource='nova.memory')
        except Exception as e:
            return 1

        return resource_type.default_price

    def sync_price(self):
        #flavor.vcpus* nova.cpu + flavor.memory*nova.mem

        if ("cpu" in self.resource
                or "memory" in self.resource):
            return None

        if self.extra == {}:

            self.extra['memory'] = 0
            self.extra['cpu'] = 0

            try:
                flavor = get_flavor(self.project.name, self.openstack_id)
                self.extra['memory'] = flavor._info['ram']
                self.extra['cpu'] = flavor._info['vcpus']
                self.extra['disk'] = flavor._info['gigabytes']

            except Exception as e:
                if not getattr(settings, "DEBUG", False):
                    pass

        try:
            price = self.extra["cpu"] * self.cpu_price
            price = price + self.extra["memory"] * self.memory_price

            self.default_price = price
            self.save()
        except Exception as e:
            raise e  # cause exception if not exist nova.cpu or nova.mem

    def save(self, *args, **kwargs):

        orig = created = None

        if self.pk is not None:
            orig = ResourceType.objects.get(pk=self.pk)
            created = False
        else:
            created = True

        super(ResourceType, self).save(*args, **kwargs)

        if not created:
            if getattr(orig, "default_price", 0) != self.default_price:
                if ("cpu" in self.resource
                        or "memory" in self.resource):
                    try:
                        send_task("sync_price", [self.project, ], {})
                    except Exception as e:
                        sync_prices(self.project)

    def __unicode__(self):
        return self.project.name + ' : ' + self.name

    class Meta:
        verbose_name = _("resource type")
        verbose_name_plural = _("resource types")


class ResourceInstanceData(models.Model):
    resource = models.ForeignKey('ResourceInstance')
    date = models.DateField(blank=True, null=True)
    closed = models.BooleanField(default=False)
    value = models.DecimalField(u"value", max_digits=18, decimal_places=3, default=0)
    price = models.DecimalField(u"price", max_digits=18, decimal_places=6, default=0)

    def update_value(self):
        if not self.closed:
            value = get_resource_data(self.resource.get_metric_path(), self.date)
            value = decimal.Decimal(str(value)) / decimal.Decimal('60')
            if self.value != value:
                self.value = value
                self.update_price()
                self.save()

    def update_price(self):
        if not self.resource.threshold or self.resource.is_over_threshold:
            disk_extra = self.resource.extra.get('disk', 1)
            default_rate = self.resource.resource_type.default_price
            self.price = (self.value - (self.resource.threshold or 0)) * \
                disk_extra * default_rate

    def close(self):
        self.closed = True
        self.save()

    def save(self, *args, **kwargs):

        super(ResourceInstanceData, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0} [{1}]".format(self.resource, self.date)

    class Meta:
        verbose_name = _("resource instance data")
        verbose_name_plural = _("resource instance data")


class ResourceInstance(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'), blank=True)
    openstack_id = models.CharField(
        max_length=255, verbose_name=_('openstack id'), blank=True, null=True)
    ceilometer_query = models.TextField(
        verbose_name=_('ceilometer query'), blank=True, null=True)
    resource_type = models.ForeignKey('ResourceType', verbose_name=_('resource type'))
    is_active = models.BooleanField(
        verbose_name=_('is active ?'), default=True, blank=True)
    extra = JSONField(verbose_name=_('extra'), null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    @property
    def threshold(self):
        if self.resource_type.default_threshold \
                and self.resource_type.default_threshold != 0:
            return self.resource_type.default_threshold
        return None

    @property
    def is_over_threshold(self):
        if self.threshold:
            start, end = _get_month_range()
            value, price = self.totals_for_period(start, end)
            if value > self.threshold:
                return True
        return False

    @property
    def data(self):
        return self.resourceinstancedata_set.all()

    def totals_for_period(self, start, end=None):
        value = price = 0
        data = self.resourceinstancedata_set.filter(
            date__range=(start, end or date.today()))
        for day in data:
            value += day.value
            price += day.price
        return value, price

    def unit_hours_for_period(self, start, end=None):
        '''returns collected values for given period'''
        value = 0
        data = self.resourceinstancedata_set.filter(
            date__range=(start, end or date.today()))
        for day in data:
            value += day.value
        return value * self.extra.get('disk', 1)

    def update_data(self):
        now = datetime.now()
        today = date.today()
        yesterday_time = now - timedelta(days=1)
        yesterday = yesterday_time.date()

        self.set_temp_data(today)

        if now.hour > 2:
            self.set_final_data(yesterday)

    def set_temp_data(self, date):
        """
        saves data for given date
        """
        data, created = ResourceInstanceData.objects.get_or_create(
            resource=self,
            date=date,
        )
        data.update_value()

    def set_final_data(self, date):
        """
        saves data for given date
        """
        try:
            data = ResourceInstanceData.objects.get(resource=self, date=date)
        except:
            data = ResourceInstanceData(resource=self, date=date)
            data.save()

        if not data.closed:
            data.close()

    @property
    def actual_data(self):
        """returns opened data
        """
        data, created = ResourceInstanceData.objects.get_or_create(
            resource=self,
            date=date.today(),
        )
        return data

    @property
    def total_hours(self):
        total = 0
        for period in self.data:
            total += period.value
        return total

    def get_metric_path(self, apendix='value'):
        if self.resource_type.resource == 'nova.instance':
            res_type = 'instance'
        elif self.resource_type.resource == 'glance.image':
            res_type = 'image'
        elif self.resource_type.resource == 'cinder.volume':
            res_type = 'volume'
        elif self.resource_type.resource == 'neutron.floating_ip':
            res_type = 'address'
        elif 'network' in self.resource_type.resource:
            res_type = self.resource_type.resource
            return 'network.%s.%s.%s.%s' % (self.resource_type.project.openstack_tenant,
                                            self.openstack_id, res_type, apendix)
        else:
            res_type = 'unknown'

        return '%s.%s.%s' % (res_type, self.openstack_id, apendix)

    def get_metric_value(self):
        value = 1
        return value

    def set_inactive(self):
        meter.send(self.get_metric_path(), 0)
        meter.send(self.get_metric_path('price'), 0)
        if self.is_active:
            self.actual_data.close()
            self.is_active = False
            self.save()

    def set_active(self, value=None):
        meter.send(self.get_metric_path(), value or self.get_metric_value())
        # calculate price and send to graphite
        price = self.total_hours * self.resource_type.default_price
        meter.send(self.get_metric_path('price'), price)
        if not self.is_active:
            self.is_active = True
            self.save()

    def save(self, *args, **kwargs):

        orig = created = None

        if self.pk is not None:
            orig = ResourceInstance.objects.get(pk=self.pk)
            created = False
        else:
            created = True

        super(ResourceInstance, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("resource instance")
        verbose_name_plural = _("resource instances")
