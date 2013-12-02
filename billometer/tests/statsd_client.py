from django.test import TestCase

import statsd
from django.conf import settings

from billometer.utils.carbon import send_data

SAMPLE_RATE = getattr(settings, "STATSD_SAMPLE_RATE", 1)
HOST = getattr(settings, "STATSD_HOST", "10.0.103.159")
PORT = getattr(settings, "PORT", 8125)


class BaseTestCase(TestCase):

    project_id = 'a2c00d588d5248d185f0bc066c1a771c'
    tenant_name = 'TCP_APP'
    server_id = "ae7c39e8-3632-4947-91a1-8ebfc5bbd86b"

    def setUp(self):
        self.con = statsd.Connection(
            host=HOST,
            port=PORT,
            disabled=False
        )
        self.gauge = statsd.Gauge("core_prod", self.con)
        self.counter = statsd.Counter("core_prod", self.con)

class GaugeTestCase(BaseTestCase):

    def test_gauge_send(self):

        #self.client.gauge('%s.nova.uptime.gauge' % self.server_id, 0)
        response = self.gauge.send('%s.nova.uptime.gauge' % self.server_id, 90)
        self.assertTrue(response)
        response = self.gauge.send('%s.nova.uptime.gauge' % self.server_id, 110)
        self.assertTrue(response)

    def test_increment_send(self):

        self.counter += 1 # that's all

    def test_carbon_send(self):

        send_data('%s.nova.uptime.carbon_test' % self.server_id, 60)