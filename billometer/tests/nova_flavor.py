from django.test import TestCase

from billometer.utils.nova_flavor import _get_client, get_flavor


class BaseTestCase(TestCase):

    project_id = 'a2c00d588d5248d185f0bc066c1a771c'
    tenant_name = 'TCP_APP'

    def setUp(self):
        self.client = _get_client(self.tenant_name)

class GetFlavorTestCase(BaseTestCase):

    def test_flavor_list(self):
        result = self.client.flavors.list()
        
        self.assertIsInstance(result, list)

    def test_flavor_get(self):
        flavor = get_flavor(self.tenant_name, "m1.small10")
        
        self.assertIsInstance(flavor._info, dict)