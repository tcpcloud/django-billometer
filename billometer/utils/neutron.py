
from django.conf import settings

from neutronclient.neutron.client import Client

from billometer.models import Project, ResourceType, ResourceInstance


def _get_client(tenant_name):

    user = settings.KEYSTONE_USER
    password = settings.KEYSTONE_PASSWORD
    auth_url = settings.OPENSTACK_KEYSTONE_URL

    client = Client("2.0",
                    username=user,
                    password=password,
                    auth_url=auth_url,
                    tenant_name=tenant_name,
                    service_type="network")

    client.format = 'json'
    return client


def sync_resource_types(project):

    resource_type_kwargs = {
        'project': project,
        'resource': 'neutron.floating_ip',
        'name': 'ip',
    }
    resource_type, created = ResourceType.objects.get_or_create(
        **resource_type_kwargs)

    resource_type.save()

    return resource_type


def sync_floating_ips(project_id):
    '''Get floating ips'''

    ip_list = []

    project = Project.objects.get(name=project_id)

    resource_type = sync_resource_types(project)

    client = _get_client(project_id)

    # load public nets
    nets = []
    for alist in client.list_networks(retrieve_all=False):
        for ip in alist['networks']:
            if ip['router:external']:
                nets.append(ip['id'])

    ips = {}
    for alist in client.list_ports(retrieve_all=False):
        for ip in alist['ports']:
            if ip['tenant_id'] == project.openstack_tenant \
                    and ip['network_id'] in nets:
                address = ip['fixed_ips'][0]['ip_address']
                if address not in ips:
                    ips[address] = {
                        'resource_type': resource_type,
                        'openstack_id': ip['name']
                    }

    # load routers
    for name, router_ip in ips.items():

        resource, created = ResourceInstance.objects.get_or_create(
            **router_ip)
        if created:
            resource.name = name
            resource.save()
        resource.set_active()
        resource.update_data()

    for ip in client.list_floatingips()['floatingips']:

        if ip['port_id'] is not None and \
                ip['tenant_id'] == project.openstack_tenant:

            server_kwargs = {
                'resource_type': resource_type,
                'openstack_id': ip['id'],
            }

            resource, created = ResourceInstance.objects.get_or_create(
                **server_kwargs)

            if created:
                resource.name = ip['floating_ip_address']
                resource.save()

            resource.set_active()
            resource.update_data()

            ip_list.append(ip['port_id'])

    return ip_list + ips.values()
