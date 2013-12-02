
import logging
from datetime import datetime, timedelta
from decimal import Decimal as D
from billometer.models import ResourceType, ResourceInstance
from billometer.conf import settings
from .graphite import get_network_stats
from .nova import _get_client

LOG = logging.getLogger(__name__)

NETWORK_RESOURCES = ['network.tx', 'network.rx']


def get_time(timestamp):
    return datetime.fromtimestamp(timestamp)


def _get_active_instances(project):

    client = _get_client(project.name)
    return [server.id for server in client.servers.list()
            if server.status == 'ACTIVE']


def _process_network_data(network_stats, project, instance_id, resource_type):
    '''Process network data and send delta to graphite'''

    if len(network_stats[resource_type]) > 0:
        data = network_stats[resource_type][0].get('datapoints', [])

        now = datetime.now()
        hour_ago = now + timedelta(hours=-1)
        data = [datum for datum in data
                if get_time(datum[1]) > hour_ago and get_time(datum[1]) < now]
        # substraction of first and last value (value, timestamp,)
        first = data[0][0]
        last = data[-2][0]
        if first and last:
            delta = last - first
            resource_type = ResourceType.objects.get(
                project=project, resource=resource_type, openstack_id=instance_id)
            server_kwargs = {
                'resource_type': resource_type,
                'openstack_id': instance_id,
            }

            resource, created = ResourceInstance.objects.get_or_create(**server_kwargs)

            if created:
                resource.name = '%s - %s' % (project.name, resource_type)
                resource.save()

            resource.set_active(delta)
            resource_data = resource.actual_data
            resource_data.value += D(delta)
            resource_data.update_price()
            resource_data.save()
            resource.update_data()
        return data

    return False


def sync_network(project):
    '''get or create network resources'''

    instances = _get_active_instances(project)

    for i, instance_id in enumerate(instances):

        for network_resource in NETWORK_RESOURCES:
            kwargs = {
                'resource': network_resource,
                'name': network_resource,
                'project': project,
                'openstack_id': instance_id,
                'default_price': D(
                    settings.EXTRA_RESOURCES[network_resource].get('price_rate', '1')),
            }
            threshold = settings.EXTRA_RESOURCES[network_resource].get('threshold', None)
            if threshold:
                kwargs['default_threshold'] = threshold
            resource, created = ResourceType.objects.get_or_create(
                resource=network_resource,
                project=project,
                openstack_id=instance_id,
                defaults=kwargs)

    for network_resource in NETWORK_RESOURCES:
        kwargs = {
            'resource': network_resource,
            'name': network_resource,
            'project': project,
            'openstack_id': project.openstack_tenant,
            'default_price': D(
                settings.EXTRA_RESOURCES[network_resource].get('price_rate', '1')),
        }
        threshold = settings.EXTRA_RESOURCES[network_resource].get('threshold', None)
        if threshold:
            kwargs['default_threshold'] = threshold
        resource, created = ResourceType.objects.get_or_create(
            resource=network_resource,
            openstack_id=project.openstack_tenant,
            project=project,
            defaults=kwargs)


def collect_network(project):
    '''Load data from graphite and send it as new metric'''

    instances = _get_active_instances(project)

    # sync all project instances
    network_stats = get_network_stats(instances)
    _process_tenant_data(network_stats, project, 'network.rx')
    _process_tenant_data(network_stats, project, 'network.tx')

    # sync per instance
    for i, instance_id in enumerate(instances):
        network_stats = get_network_stats([instance_id])
        _process_network_data(network_stats, project, instance_id, 'network.rx')
        _process_network_data(network_stats, project, instance_id, 'network.tx')

    return instances


def _process_tenant_data(network_stats, project, resource_type):
    '''Process network data and send delta to graphite'''

    if len(network_stats[resource_type]) > 0:
        data = network_stats[resource_type][0].get('datapoints', [])

        now = datetime.now()
        hour_ago = now + timedelta(hours=-1)
        data = [datum for datum in data
                if get_time(datum[1]) > hour_ago and get_time(datum[1]) < now]
        # substraction of first and last value (value, timestamp,)
        first = data[0][0]
        last = data[-2][0]
        if first and last:
            delta = last - first
            resource_type = ResourceType.objects.get(
                project=project, resource=resource_type, openstack_id=project.openstack_tenant)
            server_kwargs = {
                'resource_type': resource_type,
                'openstack_id': project.openstack_tenant
            }

            resource, created = ResourceInstance.objects.get_or_create(**server_kwargs)

            if created:
                resource.name = '%s - %s' % (project.name, resource_type)
                resource.save()

            resource.set_active(delta)
            resource_data = resource.actual_data
            resource_data.value += D(delta)
            resource_data.update_price()
            resource_data.save()
            resource.update_data()
        return data

    return False
