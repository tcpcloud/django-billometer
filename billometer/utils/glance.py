
from keystoneclient.v2_0 import client as ksclient
from glanceclient import client

from django.conf import settings
from django.utils.text import slugify

from billometer.models import Project, ResourceType, ResourceInstance


def _get_client(project_id):

    user = settings.KEYSTONE_USER
    password = settings.KEYSTONE_PASSWORD

    auth_url = settings.OPENSTACK_KEYSTONE_URL

    keystone = ksclient.Client(
        auth_url=auth_url,
        username=user,
        password=password,
        tenant_name=project_id)

    token = keystone.auth_ref['token']['id']

    for catalog in keystone.auth_ref['serviceCatalog']:
        if catalog['name'] == 'glance':
            for endpoint in catalog['endpoints']:
                epoint = endpoint['publicURL']

    c = client.Client("1",
                      endpoint=epoint,
                      token=token)

    return c


def sync_images(project_id):

    client = _get_client(project_id)

    image_list = []

    project = Project.objects.get(name=project_id)

    for image in client.images.list():

        if image._info['status'] == 'active' \
                and image._info['is_public'] is False:

            res_type, created = ResourceType.objects.get_or_create(
                project=project, resource='glance.image', name='Image')

            server_kwargs = {
                'resource_type': res_type,
                'openstack_id': image._info['id'],

            }
            resource, created = ResourceInstance.objects.get_or_create(
                **server_kwargs)

            if created:
                resource.name = slugify(image._info['name'])
                if resource.name == '':
                    resource.name = resource.openstack_id
                resource.extra['disk'] = image._info[
                    'size'] / 1024 / 1024 / 1024
                resource.save()

            image_list.append(image._info)

    return image_list


def collect_images(project_id):

    i = 0

    project = Project.objects.get(name=project_id)

    types = project.resourcetype_set.filter(
        project=project, resource='glance.image')
    resources = ResourceInstance.objects.filter(resource_type__in=types)

    client = _get_client(project.name)

    images = client.images.list()

    active_resources = []

    for image in images:
        if image._info['status'] == 'active' \
                and image._info['is_public'] is False:
            active_resources.append(image._info['id'])

    for resource in resources:

        if resource.openstack_id in active_resources:
            i = i + 1
            resource.set_active()
            resource.update_data()
        else:
            resource.set_inactive()

    return i
