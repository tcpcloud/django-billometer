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
        flavor = {
            "vcpus": 3,
            "ram": 200
        }
        project = Project.objects.create(
            name=self.tenant_name,
            openstack_tenant=self.project_id)
        self.project =project
        self.resource_type = ResourceType.objects.create(
            name="SMALL",
            project=self.project,
            resource="nova.instance",
            flavor=flavor)
        self.resource_instance = ResourceInstance.objects.create(
            name="muj server",
            resource_type=self.resource_type,
            openstack_id=self.server_id)
        self.resource_instance_data = ResourceInstanceData.objects.get(
            resource=self.resource_instance,
            start=date.today())
        
        self.cpu = ResourceType.objects.create(
            resource="nova.cpu",
            project=project,
            name="Instance CPU",
            flavor=flavor)

        self.mem = ResourceType.objects.create(
            resource="nova.memory",
            project=project,
            name="Instance Memory",
            flavor=flavor)

class SyncPriceTestCase(BaseTestCase):

    def test_setup(self):

        self.assertEqual(
            self.cpu.default_price, u"1")

    def test_change_price(self):

        self.test_setup()
        
        cpu = self.cpu

        cpu.default_price = 4

        cpu.save()

        self.assertEqual(
            self.cpu.default_price, 4)

        self.assertEqual(
            self.mem.default_price, u"1")

        self.assertEqual(
            self.resource_type.cpu_price, 4)

        self.assertEqual(
            self.resource_type.memory_price, 1)

        self.assertEqual(
            self.resource_type.flavor["vcpus"], 3)

        self.assertEqual(
            self.resource_type.flavor["ram"], 200)

        self.assertEqual(
            self.resource_type.default_price, 4*3+200*1)