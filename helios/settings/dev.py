from .common import *



ALLOWED_HOSTS = [
    # 'https://5bd793f7.ngrok.io',
    # '5bd793f7.ngrok.io',
    'localhost',
    'dev.algonauts.in',
    'algonauts.in',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
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