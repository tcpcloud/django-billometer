VERSION = (0, 0, 3,)
__version__ = '.'.join(map(str, VERSION))

"""

send exceptions from celery tasks into sentry via raven

"""

default_app_config = 'billometer.apps.Config'


try:
    from raven.contrib.django.raven_compat.models import client
    from billometer.utils.celery import register_signal, register_logger_signal

    register_signal(client)
    register_logger_signal(client)

except:
    pass
