from django.conf import settings

from novaclient.v1_1 import client


def _get_client(project_id):

    user = settings.KEYSTONE_USER
    password = settings.KEYSTONE_PASSWORD
    auth_url = settings.OPENSTACK_KEYSTONE_URL

    return client.Client(user, password, project_id, auth_url)


def get_flavor(project_id, flavor_id):

    nova = _get_client(project_id)

    for flavor in nova.flavors.list():
        if flavor.id == flavor_id:
            return flavor

    return None
