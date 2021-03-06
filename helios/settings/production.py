from .common import *
from razorpay import Client

DEBUG = False

"""
Razorpay Variable and Declaration
"""
RAZORPAY_KEY = "rzp_test_mORiHoyolnJdWj"

client = Client(auth=(RAZORPAY_KEY, "1HoPO6AkWpoZC5NG3vgN83zp"))



ALLOWED_HOSTS = [
    'dev.algonauts.in',
    'algonauts.in',
]

SECURE_SSL_REDIRECT = True

ADMINS = [('Gaurav', 'support@algonauts.in')]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[{asctime}] {levelname} {module} [{name}:{lineno}] {process:d} {thread:d} {message}",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            # 'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            #'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'worker': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.environ.get('REDIS_ADDRESS', '127.0.0.1'), os.environ.get('REDIS_PORT', 6379))],
            "capacity":1000, 
            "expiry": 2,
        },
    },
}

CRONJOBS = [
    ('0 0 * * *', 'subscriptions.cron.check_data_consistency')
]