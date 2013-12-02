"""
http://docs.openstack.org/developer/python-keystoneclient/api/keystoneclient.v2_0.client.html
"""

from decimal import Decimal
from keystoneclient.v2_0 import client

from django.conf import settings

from billometer.utils import nova
from billometer.utils import cinder


def _get_client():

    if not getattr(settings, 'KEYSTONE_SERVICE_TOKEN', False):
        user = settings.KEYSTONE_USER
        password = settings.KEYSTONE_PASSWORD
        tenant = 'service'
        return client.Client(username=user, password=password, tenant_name=tenant, auth_url=settings.OPENSTACK_KEYSTONE_URL, insecure=True)
    else:
        return client.Client(token=settings.KEYSTONE_SERVICE_TOKEN, endpoint=settings.OPENSTACK_KEYSTONE_URL, insecure=True)


def create_user_role(keystone, tenant, role, user):

    if len(keystone.roles.roles_for_user(user.id, tenant.id)) == 0:
        keystone.roles.add_user_role(user, role, tenant)


# x
def get_service_from_catalog(catalog, service_type):
    if catalog:
        for service in catalog:
            if service.type == service_type and service.enabled:
                return service
    return None


def get_service_catalog(client=None):
    service_catalog = []
    if not client:
        client = _get_client()
        """
        auth_ref = getattr(client, "auth_ref", {})
        """
    else:
        """
        auth_ref = getattr(client, "auth_ref", {})
        """
        pass
    # TODO(majklk): v2 has serviceCatalog and v3 has only "catalog"
    """
    service_catalog = auth_ref.get("serviceCatalog", [])
    """
    return client.services.list()


def is_service_enabled(service, client=None):
    """expect service name like a compute, neutron, volume etc
    """

    service_catalog = get_service_catalog(client)
    service = get_service_from_catalog(service_catalog, service)

    if service:
        return True

    return False
#######################


def _get_resource_kwargs(project, resource_name, label):
    '''return resource kwargs with price in defaults
    this prevents recreate resource type after rate update
    '''
    return {
        'resource': resource_name,
        'project': project,
        'name': label,
        'defaults': {
            'default_price': Decimal(settings.RESOURCE_PRICE[resource_name])
        }
    }


def _get_or_create_resource(project, resource_name, label):
    '''get or create resource type'''
    from billometer.models import ResourceType
    resource, created = ResourceType.objects.get_or_create(
        **_get_resource_kwargs(
            project, resource_name, label))
    return resource


def sync_tenants():

    from billometer.models import Project

    keystone = _get_client()

    role = None
    user = None

    for raw_user in keystone.users.list():
        if raw_user.name == 'billometer':
            user = raw_user

    for raw_role in keystone.roles.list():
        if raw_role.name == 'admin':
            role = raw_role

    for tenant in keystone.tenants.list():
        project, created = Project.objects.get_or_create(
            openstack_tenant=tenant.id)
        if created:

            create_user_role(keystone, tenant, role, user)

            project.name = tenant.name
            project.description = tenant.description
            project.extra = nova.get_quotas(tenant.name, tenant.id)
            project.extra.update(cinder.get_quotas(tenant.name, tenant.id))
            project.save()

            _get_or_create_resource(project, 'nova.cpu', 'Instance CPU')

            _get_or_create_resource(project, 'nova.memory', 'Instance Memory')

            if is_service_enabled("neutron"):
                _get_or_create_resource(project, 'neutron.floating_ip', 'IP')

            _get_or_create_resource(project, 'glance.image', 'Image')
        else:
            # update
            if project.name != tenant.name:
                project.name = tenant.name
                project.save()

    return keystone.tenants.list()


def projects_for_user(user_id):

    keystone = _get_client()

    projects = []

    for tenant in keystone.tenants.list():
        if len(keystone.roles.roles_for_user(user_id, tenant.id)) > 0:
            projects.append(tenant._info)
    return projects


def roles_for_user(user_id):

    keystone = _get_client()

    roles = []

    for tenant in keystone.tenants.list():
        for role in keystone.roles.roles_for_user(user_id, tenant.id):
            roles.append(role._info)

    return roles
