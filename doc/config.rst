
=============
Configuration
=============

Billometer configuration has tree main parts:

* Base Django Configuration (Database, Auth, ..)
* Keystone
* Billometer Resources
* Billometer Worker (Worker tasks, Custom Task)

Base
----

.. code-block:: python

    ALLOWED_HOSTS = ['10.10.10.70']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'PORT': '5432',
            'HOST': '127.0.0.1',
            'NAME': 'billometer',
            'PASSWORD': 'password',
            'USER': 'billometer'
        }
    }

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
            'TIMEOUT': 120,
            'KEY_PREFIX': 'CACHE_BILLOMETER'
        }
    }

Keystone
--------

.. code-block:: python

    BROKER_URL = 'amqp://billometer:sfslkfsfe@hostname.cz:5672//billometer'

    KEYSTONE_REGION = "regionOne"

    KEYSTONE_SERVICE_TOKEN = "service token"

    KEYSTONE_USER = "billometer"

    KEYSTONE_PASSWORD = "password"

    KEYSTONE_SERVICE_ENDPOINT = "http://10.10.10.70:35357/v2.0"

    OPENSTACK_KEYSTONE_URL = KEYSTONE_SERVICE_ENDPOINT

    OPENSTACK_SSL_NO_VERIFY = True

    OPENSTACK_API_VERSIONS = {
        'identity': 2.0
    }


Billometer Resources
--------------------

.. code-block:: python

    RESOURCE_PRICE = {
        'cinder.volume': {
            '7k2_SAS': '0.008205',
            '10k_SAS': '0.027383',
            '15k_SAS': '0.034232',
            'EasyTier': '0.041082',
        },
        'nova.memory': '0.000369',
        'nova.cpu': '0.821904',
        'neutron.floating_ip': '0.136972',
        'glance.image': '0.002739',
    }

    BILLING_EXTRA_RESOURCES = {
        'network.rx': {
            'threshold': '150000',
            'price_rate': '0.000002222',
            'resource': 'network.rx',
            'label': 'Network RX'
        },
        'network.tx': {
            'threshold': '99999999999999',
            'price_rate': '0.000002222',
            'resource': 'network.tx',
            'label': 'Network TX'
        },
        '7k2_SAS': {
            'price_rate': '0.008205',
            'resource': 'cinder.volume',
            'name': '7k2_SAS',
            'label': '7k2 SAS'
        },
        '10k_SAS': {
            'price_rate': '0.027383',
            'resource': 'cinder.volume',
            'label': '10k2 SAS',
            'name': '10k_SAS',
        },
        '15k_SAS': {
            'price_rate': '0.034232',
            'resource': 'cinder.volume',
            'label': '15k2 SAS',
            'name': '15k_SAS',
        },
        'EasyTier': {
            'price_rate': '0.041082',
            'resource': 'cinder.volume',
            'label': 'Easy Tier',
            'name': 'EasyTier',
        },

    }

Billometer Worker
-----------------

In default state Billometer is configured to ``sync_all`` and ``collect_all`` which means base resource such as:

* nova - instances
* glance - images
* cinder - volumes
* neutron - ip addresses

.. code-block:: python

    CELERYBEAT_SCHEDULE = {
        'collect_all': {
            'task': 'billometer.tasks.collect_all',
            'schedule': timedelta(seconds=3600),
            'args': tuple()
        },
        'sync_all': {
            'task': 'billometer.tasks.sync_all',
            'schedule': timedelta(seconds=3600),
            'args': tuple()
        },
    }

For network IN/OUT billing enable these tasks

.. code-block:: python

    CELERYBEAT_SCHEDULE = {

        ...

        'collect_network': {
            'task': 'billometer.tasks.network.collect_network',
            'schedule': timedelta(seconds=3600),
            'args': tuple()
        },
        'sync_network': {
            'task': 'billometer.tasks.network.sync_network',
            'schedule': timedelta(seconds=3600),
            'args': tuple()
        }
    }

.. note::

    Billometer works with 1 hours period.
