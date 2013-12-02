
from datetime import date

from billometer.utils.statsd_client import meter
from celery import task

from .cinder import *
from .glance import *
from .keystone import *
from .network import *
from .nova import *
from .prices import *


@task()
def sync_all():
    projects = Project.objects.all()
    sync_keystone.delay()

    try:
        sync_nova.delay(projects=projects)
    except Exception as e:
        logger.warning(str(e))
    try:
        sync_neutron.delay(projects=projects)
    except Exception as e:
        logger.warning(str(e))
    try:
        sync_cinder.delay(projects=projects)
    except Exception as e:
        logger.warning(str(e))
    try:
        sync_glance.delay(projects=projects)
    except Exception as e:
        logger.warning(str(e))

    return 'Syncing OK'


@task()
def collect_all():
    projects = Project.objects.all()
    collect_nova.delay(projects=projects)
    collect_cinder.delay(projects=projects)
    collect_glance.delay(projects=projects)
    return 'Syncing OK'


def _get_price_metric(project, metric):

    return 'tenants.%s.%s.price' % (project.openstack_tenant, metric)


@task()
def collect_price():
    '''collect all actual prices for this day and
    push them to graphite
    '''
    from billometer.models import Project

    projects = Project.objects.all()

    time = date.today()

    for project in projects:

        data = project.get_resource_prices(time, time)

        for metric, value in data.iteritems():

            metric = _get_price_metric(project, metric)
            meter.send(metric, value)

    return 'Collected prices for projects: %s OK' % len(projects)
