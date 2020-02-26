from .common import *


DEBUG = False

"""
Razorpay Variable and Declaration
"""
RAZORPAY_KEY = "rzp_test_FwV0DxK207WiS4"

client = Client(auth=(RAZORPAY_KEY, "f82D3I70VdLkWPPOzlKteAhK"))



ALLOWED_HOSTS = [
    'dev.algonauts.in',
    'algonauts.in',
]

SECURE_SSL_REDIRECT = True

ADMINS = [('Gaurav', 'gaurav.mane@algonauts.in')]

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
        # 'applogfile': {
        #     'level': 'INFO',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': 'helios.log',
        #     'maxBytes': 1024*1024*15,  # 15MB
        #     'backupCount': 10,
        # },
        # 'workerlogfile': {
        #     'level': 'INFO',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': 'worker.log',
        #     'maxBytes': 1024*1024*15,  # 15MB
        #     'backupCount': 10,
        # },
        'console': {
            'level': 'INFO',
            # 'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'worker': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

CRONJOBS = [
    ('0 0 * * *', 'subscriptions.cron.check_data_consistency')
]