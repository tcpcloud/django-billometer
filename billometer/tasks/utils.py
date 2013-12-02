
from celery import task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@task()
def backend_cleanup():
    '''delete all task results from db'''

    from djcelery.models import TaskState
    from celery import states

    query_set = TaskState.objects.exclude(state__in=states.UNREADY_STATES)
    count = query_set.count()
    query_set.delete()

    return 'Deleted: %s task results from db OK' % count
