from django.test import TestCase
from datetime import datetime, date
from django.conf import settings
from billometer.models import ResourceInstance, ResourceInstanceData, \
    ResourceType, Project


class BaseTestCase(TestCase):

    project_id = 'a2c00d588d5248d185f0bc066c1a771c'
    tenant_name = 'TCP_APP'
    server_id = "ae7c39e8-3632-4947-91a1-8ebfc5bbd86b"

    def setUp(self):
        self.project = Project.objects.create(
            name=self.tenant_name,
            openstack_tenant=self.project_id)
        self.resource_type = ResourceType.objects.create(
            name="SMALL",
            project=self.project)
        self.resource_instance = ResourceInstance.objects.create(
            name="muj server",
            resource_type=self.resource_type,
            openstack_id=self.server_id)
        self.resource_instance_data = ResourceInstanceData.objects.create(
            resource=self.resource_instance,
            date=date.today())

        """
        self.cpu = ResourceType.objects.create(
            resource="nova.cpu",
            project=self.project,
            name="Instance CPU")
        """


class BillometerTestCase(BaseTestCase):

    def test_setup(self):

        self.assertTrue(self.resource_instance.is_active)

        self.assertEqual(
            self.resource_instance.resourceinstancedata_set.count(), 1)

    def test_get_instance_data(self):

        self.assertIsInstance(
            self.resource_instance_data, ResourceInstanceData)

    def test_turn_off(self):
        """test resource instance.is_active = False"""

        self.test_get_instance_data()
        self.assertEqual(
            self.resource_instance.resourceinstancedata_set.count(), 1)

        self.assertIsInstance(
            self.resource_instance.actual_data, ResourceInstanceData)

        self.assertTrue(self.resource_instance.is_active)

        self.assertIsNone(
            self.resource_instance.actual_data.end)

        self.resource_instance.set_inactive()

        self.assertFalse(self.resource_instance.is_active)
        self.assertEquals(
            self.resource_instance.resourceinstancedata_set.all()[0].end, date.today())

        #self.resource_instance_data.end = date.today()
        # self.resource_instance_data.save()

        self.assertTrue(
            self.resource_instance.set_active())

        self.assertEqual(
            self.resource_instance.resourceinstancedata_set.count(), 2)

    def test_increment_hours_data(self):

        self.test_get_instance_data()

        self.assertEquals(
            self.resource_instance.actual_data.value, 0)

        result = self.resource_instance.actual_data.increment_value()

        self.assertEquals(
            result, 1)

        self.resource_instance.set_inactive()

        self.assertFalse(self.resource_instance.is_active)

    def test_hours_sum(self):

        resource_instance_data = self.resource_instance_data
        resource_instance_data.value = 24
        resource_instance_data.save()
        
        value, price = self.resource_instance.totals_for_period(date.today(), date.today())

        self.assertEquals(value, 24)