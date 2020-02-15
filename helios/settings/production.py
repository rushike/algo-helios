from .common import *

DEBUG = False

ALLOWED_HOSTS = [
    'dev.algonauts.in',
    'algonauts.in',
]

SECURE_SSL_REDIRECT = True
CRONJOBS = [
    ('0 0 * * *', 'subscriptions.cron.check_data_consistency')
]