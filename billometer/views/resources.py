import datetime
import decimal
import logging
from django.utils import six
import simplejson
from billometer.models import Project, ResourceInstance, ResourceType
from billometer.utils.graphite import get_server
from billometer.utils.keystone import projects_for_user
from billometer.utils.memonized import memoyield
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from billometer.conf import settings

from .utils import JSONResponse, now_iso, handle_exception

LOG = logging.getLogger(__name__)


@memoyield
def get_data(user_id, start_date=None, end_date=None):

    if start_date is None:
        start_date = datetime.date.today()

    if end_date is None:
        end_date = datetime.date.today()

    project_names = []

    projects = projects_for_user(user_id)

    for project in projects:
        project_names.append(project['name'])

    project_list = []

    projects = Project.objects.filter(name__in=project_names)

    for project in projects:

        instance = ResourceInstance.objects.filter(
            resource_type__project=project, resource_type__resource='nova.instance', is_active=True)
        volume = ResourceInstance.objects.filter(
            resource_type__project=project, resource_type__resource='cinder.volume', is_active=True)
        address = ResourceInstance.objects.filter(
            resource_type__project=project, resource_type__resource='neutron.floating_ip', is_active=True)
        image = ResourceInstance.objects.filter(
            resource_type__project=project, resource_type__resource='glance.image', is_active=True)

        project_kwargs = {
            'name': project.name,
            'uuid': project.openstack_tenant,
            'instance_count': instance.count(),
            'instance_price': project.get_resource_price('nova.instance', start_date, end_date),
            'volume_count': volume.count(),
            'volume_price': project.get_resource_price('cinder.volume', start_date, end_date),
            'address_count': address.count(),
            'address_price': project.get_resource_price('neutron.floating_ip', start_date, end_date),
            'image_count': image.count(),
            'image_price': project.get_resource_price('glance.image', start_date, end_date),
        }

        """
        for r_name, resource in six.iteritems(settings.EXTRA_RESOURCES):
            try:
                _value, _price = project.get_resource_data(
                    resource["resource"], start_date, end_date)
                project_kwargs['%s.count' % resource["resource"]] = _value
                project_kwargs['%s.price' % resource["resource"]] = _price
            except Exception as e:
                LOG.error(str(e))
        """

        project_list.append(project_kwargs)
    return project_list


def _get_resource_list(project):
    resource_list = []

    _resources = ResourceType.objects.filter(
        project=project).exclude(resource="nova.instance")

    for resource in _resources:
        resource_list.append({
            'id': resource.id,
            'name': resource.name,
            'resource': resource.resource,
            'default_price': resource.default_price,
            'default_threshold': resource.default_threshold,
        })

    return resource_list


@csrf_exempt
def resource_list(request, project_id):
    resource_list = []
    project = Project.objects.get(openstack_tenant=project_id)

    if request.method == "GET":
        resource_list = _get_resource_list(project)
    elif request.method == "POST":
        data = simplejson.loads(request.body)

        for resource in data:

            r = ResourceType.objects.get(id=resource["id"])

            default_threshold = decimal.Decimal(str(resource["default_threshold"]))
            default_price = decimal.Decimal(str(resource["default_price"]))

            r.default_threshold = default_threshold
            r.default_price = default_price
            r.save()

        resource_list = _get_resource_list(project)

    return JSONResponse(resource_list)


class ResourceMixin(object):

    resource_type = "unknown"
    project = None

    @property
    def filter_kwargs(self):
        filter_kwargs = {
            "resource_type__project": self.project,
            "resource_type__resource": self.resource_type
        }
        return filter_kwargs

    @property
    def resources(self):
        resources = ResourceInstance.objects.filter(
            **self.filter_kwargs).distinct()
        return [r for r in resources
                if r.total_hours > 0]


class BaseResourceView(ResourceMixin, generic.View):

    """
    A base view for displaying a resource list
    """

    @handle_exception
    def get(self, request, *args, **kwargs):
        result_list = []

        self.project = Project.objects.get(openstack_tenant=self.kwargs['project_id'])
        resource_instances = self.resources

        start = self.kwargs.get('start_date', datetime.date.today())
        end = self.kwargs.get('end_date', datetime.date.today())

        for resource in resource_instances:
            value, price = resource.totals_for_period(start, end)
            result_list.append({
                'name': resource.name,
                'uuid': resource.openstack_id,
                'type': resource.resource_type.name,
                'size': resource.extra.get('disk', None),
                'active': resource.is_active,
                'value': value,
                'price': price,
            })

        return JSONResponse(result_list)


class InstanceResourceView(BaseResourceView):

    """
    Nova instance resource list
    """

    resource_type = "nova.instance"

    def get(self, request, *args, **kwargs):
        result_list = []

        start = self.kwargs.get('start_date', now_iso())
        end = self.kwargs.get('end_date', now_iso())

        self.project = Project.objects.get(openstack_tenant=self.kwargs['project_id'])

        resource_instances = self.resources

        start_str = '00:00_%s' % start.replace("-", "")
        if now_iso() == end:
            end_str = '00:00_%s' % end.replace("-", "")
        else:
            end_str = '23:59_%s' % end.replace("-", "")

        for resource in resource_instances:

            data = get_server(resource.openstack_id, start_str, end_str)

            network_in = '-'
            network_out = '-'
            if data['network_in'] != '-':
                network_in = data['network_in'] / 1048576
            if data['network_out'] != '-':
                network_out = data['network_out'] / 1048576

            value, price = resource.totals_for_period(start, end)
            result_list.append({
                'name': resource.name,
                'uuid': resource.openstack_id,
                'type': resource.resource_type.name,
                'active': resource.is_active,
                'value': value,
                'price': price,
                'storage_read': data['storage_read'],
                'storage_write': data['storage_write'],
                'network_in': network_in,
                'network_out': network_out,
            })

        return JSONResponse(result_list)


class VolumeResourceView(BaseResourceView):

    """
    Neutron network resource list
    """

    resource_type = "cinder.volume"


class NetworkResourceView(BaseResourceView):

    """
    Neutron network resource list
    """

    resource_type = ["network.rx", "network.tx"]

    @property
    def filter_kwargs(self):
        filter_kwargs = {
            "resource_type__project": self.project,
            "resource_type__resource__in": self.resource_type
        }
        return filter_kwargs


class AddressResourceView(BaseResourceView):

    """
    Neutron network resource list
    """

    resource_type = "neutron.floating_ip"


class ImageResourceView(BaseResourceView):

    """
    Glance images resource list
    """

    resource_type = "glance.image"
