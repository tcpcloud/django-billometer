from django.test import TestCase

from billometer.utils.neutron import _get_client


class BaseTestCase(TestCase):

    project_id = 'a2c00d588d5248d185f0bc066c1a771c'
    tenant_name = 'admin'

    def setUp(self):
        self.client = _get_client(self.tenant_name)

class NetworkListTestCase(BaseTestCase):

    def test_volume_list(self):
        """login into keystone and gfet volume list"""
        result = self.client.list_floatingips()['floatingips']
        
        self.assertIsInstance(result, list)
