
import logging
from django.conf import settings

from novaclient.v1_1 import client as novaclient

from billometer.models import Project, ResourceType, ResourceInstance


LOG = logging.getLogger(__name__)


def _get_client(project_id):

    user = settings.KEYSTONE_USER
    password = settings.KEYSTONE_PASSWORD
    auth_url = settings.OPENSTACK_KEYSTONE_URL

    return novaclient.Client(user, password, project_id, auth_url)


def get_quotas(project_name, project_id):

    nova = _get_client(project_name)
    return {
        'memory': nova.quotas.get(project_id)._info['ram'],
        'cpu': nova.quotas.get(project_id)._info['cores']
    }


def set_quotas(project_name, project_id, data):

    nova = _get_client(project_name)
    quotas = nova.quotas.update(project_id, **data)
    return quotas


def sync_flavors(project_name):

    nova = _get_client(project_name)

    flavor_list = []

    project = Project.objects.get(name=project_name)

    for flavor in nova.flavors.list():
        flavor_kwargs = {
            'resource': 'nova.instance',
            'project': project,
            'openstack_id': flavor.id
        }
        resource, created = ResourceType.objects.get_or_create(**flavor_kwargs)
        if created:
            resource.name = flavor.name
            resource.extra['memory'] = flavor._info['ram']
            resource.extra['cpu'] = flavor._info['vcpus']
            resource.extra['disk'] = flavor._info.get('gigabytes', 0)
            resource.save()
            resource.sync_price()

        flavor_list.append(flavor._info)

    return flavor_list


def sync_servers(project_id):
    nova = _get_client(project_id)
    items = []
    errors = []

    project = Project.objects.get(name=project_id)

    for server in nova.servers.list():

        if server._info['status'] == 'ACTIVE':
            try:
                LOG.debug(server._info)
                flavor = ResourceType.objects.get(
                    project=project, resource='nova.instance',
                    openstack_id=server._info['flavor']['id'])
            except:
                errors.append(server._info)
                continue

            server_kwargs = {
                'resource_type': flavor,
                'openstack_id': server._info['id'],
            }

            resource, created = ResourceInstance.objects.get_or_create(**server_kwargs)

            if created:
                resource.name = server.name
                resource.save()

            items.append(server._info)

    return items, errors


def collect_servers(project_id):

    i = 0

    project = Project.objects.get(name=project_id)

    types = project.resourcetype_set.filter(project=project, resource='nova.instance')
    resources = ResourceInstance.objects.filter(resource_type__in=types)

    client = _get_client(project.name)

    servers = client.servers.list()

    active_resources = []

    for server in servers:
        if server._info['status'] == 'ACTIVE':
            active_resources.append(server._info['id'])

    for resource in resources:

        if resource.openstack_id in active_resources:
            i = i + 1
            resource.set_active()
            resource.update_data()

        else:
            resource.set_inactive()

    return i


def test_servers(project_id):

    nova = _get_client(project_id)

    return nova.servers.list()


def measure_instance_disk_usage(project_id, instance_id):
    pass


def servers_for_project(project_id):

    nova = _get_client(project_id)

    return nova.servers.list()
