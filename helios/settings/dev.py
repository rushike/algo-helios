from .common import *

ALLOWED_HOSTS = [
    'localhost',
    'dev.algonauts.in',
    'algonauts.in',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'algonauts',
        'USER': 'algonauts',
        'PASSWORD': 'okokok99',
        'HOST': 'localhost',
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
    },
    'loggers': {
        'django': {
            'handlers': ['file_1'],
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

CRONJOBS = [
    ('*/1 * * * *', 'subscriptions.cron.check_data_consistency')
]

