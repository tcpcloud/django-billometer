
import requests

import time

import datetime

GRAPHITE_ENDPOINT = "http://10.0.103.159:80"

def get_server_data(resource_id):

    fromd = '00:00_20140815'
    tod = '00:00_20140820'

    uptime = 'scale(integral(summarize(transformNull(offset(scale(core_prod.ae7c39e8-3632-4947-91a1-8ebfc5bbd86b.libvirt.virt_cpu_total.value,0),1)),"1h")), "0.016666667")' % resource_id
#    start_line = 'transformNull(offset(scale(core_prod.ae7c39e8-3632-4947-91a1-8ebfc5bbd86b.libvirt.virt_cpu_total.value,0),1))'
#    start_line = 'integral(transformNull(offset(scale(timeShift(core_prod.%s.libvirt.virt_cpu_total.value,"%sd"),0),1)))' % (resource_id, days)
#    end_line = 'integral(transformNull(offset(scale(core_prod.%s.libvirt.virt_cpu_total.value,0),1)))' % resource_id

    targets = {
        'uptime': uptime,
#        'uptime2': end_line,
#        'uptime3': 'sumSeries(%s, %s)' % (start_line, end_line),
#        'storage': 'sumSeries(core_prod.%s.libvirt.disk_ops-*.*)' % resource_id,
#        'network': 'sumSeries(core_prod.%s.libvirt.if packets-*.*)' % resource_id
    }

    output = {}

    for metric, target in targets.iteritems():
        payload = {
            'target': target,
            'format': 'json',
            'from': fromd,
            'until': tod
        }

        url = '%s/render' % GRAPHITE_ENDPOINT

        print payload

        response = requests.get(url, params=payload)
        metrics = response.json()

        print metrics

        points = metrics[0]['datapoints']
        print points
        for point in points:
            print(
                datetime.datetime.fromtimestamp(
                    point[1]
                ).strftime('%Y-%m-%d %H:%M:%S')
            )
            print point[0]

        output[metric] = points[-1][0] #- points[1][0]

    return output

RESOURCE = 'ae7c39e8-3632-4947-91a1-8ebfc5bbd86b'

output = get_server_data(RESOURCE)

for item, values in output.iteritems():
    print item
    print values
