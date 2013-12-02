
import statsd

SAMPLE_RATE = 1
HOST = "10.10.10.180"
PORT = 8125

statsd_connection = statsd.Connection(
    host=HOST,
    port=PORT,
    sample_rate=SAMPLE_RATE,
    disabled=False
)

PREFIX = 'gauge.test'

gauge = statsd.Gauge(PREFIX, statsd_connection)

gauge.send('metric1', 50)
gauge.send('metric3', 10)
