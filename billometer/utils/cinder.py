
import logging
from decimal import Decimal

import six
from billometer.models import Project, ResourceInstance, ResourceType
from cinderclient import v1
from django.conf import settings
from django.utils.text import slugify

LOG = logging.getLogger(__name__)


def _get_client(project_id):

    user = settings.KEYSTONE_USER
    password = settings.KEYSTONE_PASSWORD

    api_key = settings.KEYSTONE_SERVICE_TOKEN
    auth_url = settings.OPENSTACK_KEYSTONE_URL

    return v1.client.Client(user, password, project_id, auth_url, service_type="volume")


def get_quotas(project_name, project_id):

    cinder = _get_client(project_name)
    quotas = cinder.quotas.get(project_id)
    LOG.debug(quotas._info)
    _quotas = {}

    for key, value in six.iteritems(quotas._info):
        if "gigabytes_" in key:
            name = key.split("_")[1]
            _quotas["disk_" + str(name)] = quotas._info[key]

    return _quotas


def set_quotas(project_name, project_id, data):

    cinder = _get_client(project_name)

    return cinder.quotas.update(project_id, **data)


def sync_volume_types(project_id):

    client = _get_client(project_id)

    volume_type_list = []

    project = Project.objects.get(name=project_id)

    LOG.debug(client.volume_types.list())

    for volume_type in client.volume_types.list():
        volume_type_kwargs = {
            'resource': 'cinder.volume',
            'project': project,
            'name': volume_type.name
        }
        resource, created = ResourceType.objects.get_or_create(
            **volume_type_kwargs)

        if created:
            resource.openstack_id = volume_type.id
            resource.default_price = Decimal(
                settings.RESOURCE_PRICE['cinder.volume'].get(volume_type.name, '1'))
            resource.save()

        volume_type_list.append(volume_type._info)

    return volume_type_list


def sync_volumes(project_id):

    client = _get_client(project_id)

    volume_list = []

    project = Project.objects.get(name=project_id)

    for volume in client.volumes.list():

        if volume._info['status'] in ['available', 'in-use']:

            try:
                resource_type = ResourceType.objects.get(
                    project=project, resource='cinder.volume',
                    name=volume._info['volume_type'])
            except Exception as e:
                LOG.exception('Volume type %s not '
                              'found in %s - raised %s' % (
                                  volume._info['volume_type'],
                                  volume._info, str(e)))
            else:
                server_kwargs = {
                    'resource_type': resource_type,
                    'openstack_id': volume._info['id'],
                }

                resource, created = ResourceInstance.objects.get_or_create(
                    **server_kwargs)

                if created:
                    resource.name = slugify(volume._info['display_name'])
                    if resource.name == '':
                        resource.name = resource.openstack_id
                    resource.extra['disk'] = volume._info['size']
                    resource.save()

                volume_list.append(volume._info)

    return volume_list


def collect_volumes(project_id):

    i = 0

    project = Project.objects.get(name=project_id)

    types = project.resourcetype_set.filter(
        project=project, resource='cinder.volume')
    resources = ResourceInstance.objects.filter(resource_type__in=types)

    client = _get_client(project.name)

    volumes = client.volumes.list()

    active_resources = []

    for volume in volumes:
        if volume._info['status'] in ['available', 'in-use']:
            active_resources.append(volume._info['id'])

    for resource in resources:

        if resource.openstack_id in active_resources:
            i = i + 1
            resource.set_active()
            resource.update_data()
        else:
            resource.set_inactive()

    return i
