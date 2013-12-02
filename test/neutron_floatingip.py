    
from neutronclient.neutron import client

KEYSTONE_USER = "billometer"
KEYSTONE_PASSWORD = "fdsfdsfdsfdsfds"
KEYSTONE_SERVICE_ENDPOINT="http://10.0.106.30:35357/v2.0"
#KEYSTONE_SERVICE_ENDPOINT="http://10.0.106.30:5000/v2.0"

project_id = 'a2c00d588d5248d185f0bc066c1a771c'
tenant_name = 'admin'


user = KEYSTONE_USER
password = KEYSTONE_PASSWORD

auth_url = KEYSTONE_SERVICE_ENDPOINT

#neutron = client.Client('2.0', endpoint_url=auth_url, token=OS_TOKEN)
neutron = client.Client('2.0', auth_url=auth_url, username=user, password=password, tenant_name=tenant_name)
neutron.format = 'json'

print neutron

i = 0
for alist in neutron.list_floatingips(retrieve_all=False):
    for ip in alist['floatingips']:
        i += 1
        print i
        print ip

i = 0

for ip in neutron.list_floatingips()['floatingips']:
    i += 1
    print i
    print ip
#    neutron.show_floating_ip(ip['id'])
