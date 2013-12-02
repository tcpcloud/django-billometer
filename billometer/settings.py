# -*- coding: utf-8 -*-

from os.path import join, dirname, abspath, normpath

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/var/lib/billometer/db.sqlite3',
    }
}

OPENSTACK_SSL_NO_VERIFY = True

OPENSTACK_API_VERSIONS = {
    'identity': 2.0
}

USE_TZ = True

OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = False
OPENSTACK_KEYSTONE_DEFAULT_DOMAIN = 'Default'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Admin', 'mail@newt.cz'),
)

MANAGERS = ADMINS

SITE_ID = 1
SITE_NAME = 'billometer'

TIME_ZONE = 'Europe/Prague'

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', 'EN'),
)

USE_I18N = True

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'billometer.urls'

INSTALLED_APPS = (
    'django',
    'django_extensions',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',
    'rest_framework',
    'openstack_auth',
    'billometer',
    'djcelery',
)

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
}

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'openstack_auth.backend.KeystoneBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ]
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

try:
    with open("/etc/billometer/settings.py") as f:
        code = compile(f.read(), "/etc/billometer/settings.py", 'exec')
        exec(code)
except IOError:
    pass

if hasattr(globals(), "LOCAL_INSTALLED_APPS"):
    INSTALLED_APPS += LOCAL_INSTALLED_APPS
