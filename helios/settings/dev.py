from .common import *



ALLOWED_HOSTS = [
    'localhost',
    'dev.algonauts.in',
    'algonauts.in',
]

ABSOLUTE_URL_HOME = 'http://localhost:8000/'

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

EMAIL_HOST_USER = 'javaproject1024@gmail.com'
EMAIL_HOST_PASSWORD = 'JavaProjec'

