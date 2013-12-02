
from keystoneclient.v2_0 import client as ksclient
from glanceclient import client

KEYSTONE_USER = "billometer"
KEYSTONE_PASSWORD = "fdsfdsfdsfdsfds"
KEYSTONE_SERVICE_ENDPOINT="http://10.0.106.30:35357/v2.0"
#KEYSTONE_SERVICE_ENDPOINT="http://10.0.106.30:5000/v2.0"

project_id = 'a2c00d588d5248d185f0bc066c1a771c'
project_name = 'TCP_APP'

user = KEYSTONE_USER
password = KEYSTONE_PASSWORD

auth_url = KEYSTONE_SERVICE_ENDPOINT

keystone = ksclient.Client(auth_url=auth_url, username=user, password=password, tenant_name=project_name)

token = keystone.auth_ref['token']['id']

print token

for catalog in keystone.auth_ref['serviceCatalog']:
    if catalog['name'] == 'glance':
        for endpoint in catalog['endpoints']:
            epoint = endpoint['publicURL']

print epoint

cclient = client.Client("1", 
     endpoint=epoint,
     token=token)

print cclient

print cclient.images.list()

for image in cclient.images.list():

    if image._info['status'] == 'active' and image._info['is_public'] == False:
    
        print image
