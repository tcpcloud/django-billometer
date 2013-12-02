

import statsd
from django.conf import settings

HOST = getattr(settings, "STATSD_HOST", "10.0.103.159")
PORT = getattr(settings, "STATSD_PORT", 8125)
SAMPLE_RATE = getattr(settings, "STATSD_SAMPLE_RATE", 1)
PREFIX = getattr(settings, "STATSD_PREFIX", 'billometer')

statsd_connection = statsd.Connection(
    host=HOST,
    port=PORT,
    sample_rate=SAMPLE_RATE,
    disabled=False
)

meter = statsd.Gauge(PREFIX, statsd_connection)
