from django.conf import settings

import datetime

import requests


def collect_server(project_id, resource_id):

    targets = {
        'compute': 'core_prod.%s.nova.uptime.value)' % resource_id,
        'storage': 'integral(nonNegativeDerivative(sumSeries(core_prod.%s.libvirt.disk_ops-*.*)))' % resource_id,
        'network': 'integral(nonNegativeDerivative(sumSeries(core_prod.%s.libvirt.if packets-*.*)))' % resource_id
    }

    output = {}

    for metric, target in targets.iteritems():
        payload = {
            'target': target,
            'format': 'json',
            'from': '-600min'
        }

        url = '%s/render' % settings.GRAPHITE_ENDPOINT

        response = requests.get(url, params=payload)

        output[metric] = response.json()

#        send_data('target', data[-1])
    return output


def get_network_stats(instances):

    targets = {
        'network.rx': 'integral(nonNegativeDerivative(sumSeries(default_prd.{%s}.libvirt.if_octets.*.rx)))',
        'network.tx': 'integral(nonNegativeDerivative(sumSeries(default_prd.{%s}.libvirt.if_octets.*.tx)))'
    }

    output = {}

    for metric, target in targets.iteritems():
        payload = {
            'target': target % ','.join(instances),
            'format': 'json',
            'from': '-120min'
        }

        url = '%s/render' % settings.GRAPHITE_ENDPOINT

        response = requests.get(url, params=payload)

        output[metric] = response.json()

    return output


def get_server(resource_id, date_from, date_until):

    targets = {
        #        'compute': 'scale(integral(summarize(transformNull(offset(scale(core_prod.%s.libvirt.virt_cpu_total.value,0),1)),"1h")), "0.016666667")' % resource_id,
        'storage_write': 'integral(nonNegativeDerivative(sumSeries(core_prod.%s.libvirt.disk_ops-*.write)))' % resource_id,
        'storage_read': 'integral(nonNegativeDerivative(sumSeries(core_prod.%s.libvirt.disk_ops-*.read)))' % resource_id,
        'network_in': 'integral(nonNegativeDerivative(sumSeries(core_prod.%s.libvirt.if_octets-*.rx)))' % resource_id,
        'network_out': 'integral(nonNegativeDerivative(sumSeries(core_prod.%s.libvirt.if_octets-*.tx)))' % resource_id
    }

    output = {}

    for metric, target in targets.iteritems():
        payload = {
            'target': target,
            'format': 'json',
            'from': date_from,
            'until': date_until
        }

        url = '%s/render' % settings.GRAPHITE_ENDPOINT

        response = requests.get(url, params=payload)

        try:
            metrics = response.json()
        except Exception, e:
            metrics = []

        if len(metrics) > 0:
            points = metrics[0]['datapoints']
        else:
            output[metric] = '-'
            continue

        if metric == 'compute':
            output[metric] = points[-1][0]
        else:
            if points[-1][0] == None:
                output[metric] = '-'
            else:
                if points[0][0] == None:
                    point0 = 0
                else:
                    point0 = points[0][0]
                output[metric] = points[-1][0] - point0

    return output


def get_resource_data(resource_target, date):

    target = 'integral(transformNull(stats.gauges.billometer.%s))' % resource_target,

    time_from = datetime.datetime.combine(date, datetime.datetime.min.time())
    time_until = time_from + datetime.timedelta(days=1)

    date_from = '00:00_%s' % str(time_from.date()).replace("-", "")
    date_until = '00:01_%s' % str(time_until.date()).replace("-", "")

    payload = {
        'target': target,
        'format': 'json',
        'from': date_from,
        'until': date_until
    }

    url = '%s/render' % settings.GRAPHITE_ENDPOINT
#    url = '%s/render' % 'http://10.0.103.159'

    response = requests.get(url, params=payload)
    metrics = response.json()

    if len(metrics) > 0:
        points = metrics[0]['datapoints']
    else:
        output = -2
        return output

    if points[-1][0] == None:
        output = -1
    else:
        if points[0][0] == None:
            point0 = 0
        else:
            point0 = points[0][0]
        output = points[-1][0] - point0

    return output
