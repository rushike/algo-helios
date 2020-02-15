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

CRONJOBS = [
    ('1 * * * *', 'subscriptions.cron.check_data_consistency')
]

