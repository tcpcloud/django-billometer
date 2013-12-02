
from billometer.models import Project
from billometer.utils import cinder, is_service_enabled
from billometer.utils.statsd_client import meter
from celery import task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@task()
def sync_cinder(projects=None):
    logger = sync_cinder.get_logger()

    if not is_service_enabled("volume"):
        return "Cinder is disabled. Sync was skipped."

    i = 0
    for project in projects or Project.objects.all():
        try:

            i += 1

            cinder.sync_volume_types(project.name)
            volumes = cinder.sync_volumes(project.name)
            logger.info('%s VOLUMES: %s' % (project.name, len(volumes)))
            meter.send('counter.%s.volume' %
                       project.openstack_tenant, len(volumes))

        except Exception as e:
            logger.warning(
                'Error %s raised during %s processing' % (str(e), project))

    return 'OK: %i' % i


@task()
def collect_cinder(projects=None):
    logger = collect_cinder.get_logger()

    if not is_service_enabled("volume"):
        return "Cinder is disabled. Collect was skipped."
    i = 0
    for project in projects or Project.objects.all():
        i += 1
        volumes = cinder.collect_volumes(project.name)
        logger.info('%s collect volumes: %s' % (project.name, volumes))
    return 'OK: %s' % i
