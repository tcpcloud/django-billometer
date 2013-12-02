
from billometer.models import ResourceType
from celery import task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@task(name="sync_price")
def sync_price(project):

    query_set = ResourceType.objects \
                            .filter(project=project,
                                    resource="nova.instance")

    for resource_type in query_set.all():
        resource_type.sync_price()

    return 'Sync price on project: %s OK' % project


def _get_price_metric(project, metric):

    return 'tenants.%s.%s.price' % (project.openstack_tenant, metric)
