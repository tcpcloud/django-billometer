
from billometer.models import Project
from billometer.utils import glance
from billometer.utils.statsd_client import meter
from celery import task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@task()
def sync_glance(projects=None):
    logger = sync_glance.get_logger()

    i = 0

    for project in (projects or Project.objects.all()):

        images = glance.sync_images(project.name)
        i += 1
        logger.info('%s IMAGES: %s' % (project.name, len(images)))
        meter.send('counter.%s.image' % project.openstack_tenant, len(images))

    return 'OK: %s' % i


@task()
def collect_glance(projects=None):
    logger = collect_glance.get_logger()

    i = 0

    for project in (projects or Project.objects.all()):

        images = glance.collect_images(project.name)
        i += 1
        logger.info('%s collect images: %s' % (project.name, images))

    return 'OK: %s' % i
