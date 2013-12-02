    
from novaclient.v1_1 import client

KEYSTONE_USER = "billometer"
KEYSTONE_PASSWORD = "fdsfdsfdsfdsfds"
KEYSTONE_SERVICE_ENDPOINT="http://10.0.106.30:35357/v2.0"
#KEYSTONE_SERVICE_ENDPOINT="http://10.0.106.30:5000/v2.0"

project_id = 'a2c00d588d5248d185f0bc066c1a771c'
tenant_name = 'TCP_APP'

user = KEYSTONE_USER
password = KEYSTONE_PASSWORD

auth_url = KEYSTONE_SERVICE_ENDPOINT

#neutron = client.Client('2.0', endpoint_url=auth_url, token=OS_TOKEN)
nova = client.Client(user, password, tenant_name, auth_url)

print nova

i = 0

for ip in nova.floating_ips.list():
    i += 1
    print i
    print ip._info['ip']
#    neutron.show_floating_ip(ip['id'])
