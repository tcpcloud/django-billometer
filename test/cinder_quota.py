	
from cinderclient import v1

KEYSTONE_USER = "billometer"
KEYSTONE_PASSWORD = "fdsfdsfdsfdsfds"
KEYSTONE_SERVICE_ENDPOINT="http://10.0.106.30:35357/v2.0"
#KEYSTONE_SERVICE_ENDPOINT="http://10.0.106.30:5000/v2.0"

project_id = 'a2c00d588d5248d185f0bc066c1a771c'
project_id = 'TCP_APP'
user = KEYSTONE_USER
password = KEYSTONE_PASSWORD

auth_url = KEYSTONE_SERVICE_ENDPOINT

client = v1.client.Client(user, password, project_id, auth_url, service_type="volume")

volume_list = []

print client

print client.volumes.list()

print client.quotas.get(project_id)._info
