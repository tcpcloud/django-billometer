
from billometer.models import Project
from celery import task
from billometer.utils.statsd_client import meter
from celery.utils.log import get_task_logger
from billometer.utils import network, is_service_enabled, neutron

logger = get_task_logger(__name__)


@task()
def sync_neutron(projects=None):
    logger = sync_neutron.get_logger()
    i = 0

    if is_service_enabled("network"):
        for project in (projects or Project.objects.all()):
            i = i + 1

            ips = neutron.sync_floating_ips(project.name)
            logger.info('%s IPS: %s' % (project.name, ips))

        try:
            logger.info('%s IPS: %s' % (project.name, len(ips)))
            meter.send('counter.%s.address' %
                       project.openstack_tenant, len(ips))
        except Exception as e:
            logger.warning(str(e))

        return 'OK: %i' % i
    return "Neutron is disabled. Sync was skipped."


@task()
def collect_network(projects=None):
    logger = collect_network.get_logger()
    i = 0

    for project in (projects or Project.objects.all()):
        i = i + 1

        try:
            network.collect_network(project)
        except Exception as e:
            logger.exception(e)

    return 'OK: %s projects' % i


@task()
def sync_network(projects=None):
    logger = collect_network.get_logger()
    i = 0

    for project in (projects or Project.objects.all()):
        i = i + 1

        try:
            network.sync_network(project)
        except Exception as e:
            logger.exception(e)

    return 'OK: %s projects' % i
