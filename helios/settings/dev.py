import sys
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())



from .common import *
from razorpay import Client
import django
from django.utils.log import DEFAULT_LOGGING

"""
Razorpay Variable and Declaration
"""
RAZORPAY_KEY = "rzp_test_FwV0DxK207WiS4"

client = Client(auth=(RAZORPAY_KEY, "f82D3I70VdLkWPPOzlKteAhK"))



"""
Allowed Host for sites
"""
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

"""
Local database credentials
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'algonauts',
        'USER': 'algonauts',
        'PASSWORD': 'algonauts@123',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'janus' : {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'janusdb',
        'USER': 'algonauts',
        'PASSWORD': 'algonauts@123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'helios_db',
        'USER': 'sysadmin',
        'PASSWORD': 'A@lg0@dm!n#2@1',
        'HOST': '104.211.115.250',
        'PORT': '5432',
    },
      'janus' : {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'janus_db',
        'USER': 'sysadmin',
        'PASSWORD': 'A@lg0@dm!n#2@1',
        'HOST': '104.211.115.250',
        'PORT': '5432',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file_1': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
        'file_2': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'worker.log',
        },
        'file_3': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'normal.log',
        },
        
    },
    'loggers': {
        'django': {
            'handlers': ['file_1'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'normal': {
            'handlers': ['file_3'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'worker': {
            'handlers': ['file_2'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

DEFAULT_LOGGING['loggers'][''] = {
    'handlers': ['console'],
    'level': 'DEBUG',
    'propagate': True
}


# Setting InMemory Channel Layer, since default self.channel_layer, channels.layers.get_channel_layer() was having output none
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels.layers.InMemoryChannelLayer',
#     },
# }
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.environ.get('REDIS_ADDRESS', '127.0.0.1'), os.environ.get('REDIS_PORT', 6379))],
            "capacity":20000, 
            "expiry":10,
        },
    },
}

CRONJOBS = [
    ('*/1 * * * *', 'subscriptions.cron.check_data_consistency', '>> worker.log')
]

CRONTAB_COMMAND_SUFFIX = '2>&1'