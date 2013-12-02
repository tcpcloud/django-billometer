
from billometer.models import Project
from billometer.utils import nova
from billometer.utils.statsd_client import meter
from celery import task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@task()
def sync_nova(projects=None):
    logger = sync_nova.get_logger()
    i = 0

    for project in (projects or Project.objects.all()):
        i = i + 1

        nova.sync_flavors(project.name)
        servers, errors = nova.sync_servers(project.name)
        logger.info('%s SERVERS: %s' % (project.name, len(servers)))
        meter.send('counter.%s.instance' %
                   project.openstack_tenant, len(servers))
        logger.info('%s SERVER ERRORS: %s' % (project.name, len(errors)))

    return 'OK: %s' % i


@task()
def collect_nova(projects=None):
    logger = collect_nova.get_logger()
    i = 0

    for project in (projects or Project.objects.all()):
        i = i + 1

        servers = nova.collect_servers(project.name)
        logger.info('%s collect servers: %s' % (project.name, servers))

    return 'OK: %s' % i
