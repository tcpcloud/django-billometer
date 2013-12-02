
from celery import task
from billometer.utils.keystone import sync_tenants


@task()
def sync_keystone():
    tenants = sync_tenants()
    return 'OK: %s' % len(tenants)
