import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = '&z750(_rn%vr8bb&!yv$_ps*$m(#+^q-cq$v11pe&za-(46fl)'

ALLOWED_HOSTS = [
    'localhost',
    'dev.algonauts.in',
    'algonauts.in',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'django_extensions',
    'django_crontab',
    'crispy_forms',
    'catalog',
    'users',
    'blog',
    'products',
    'subscriptions',
    'webpush',
    'channels',
    'worker',
    'wkhtmltopdf',  # Dependency for PDF generation
    ]


SECURE_SSL_REDIRECT = False

# Algonauts User Model
AUTH_USER_MODEL = 'users.AlgonautsUser'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

SITE_ID = 1


# Allauth Variables - START

ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

LOGIN_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SUBJECT_PREFIX = '[dev user skeleton] '

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587

EMAIL_HOST_USER = 'algonauts.tech@gmail.com'
EMAIL_HOST_PASSWORD = 'duvesiehbsekfbky' #'algonauts@123'

EMAIL_USE_TLS = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_FORMS = {
'signup': 'users.forms.signup.AlgonautsSignupForm',
}

# Allauth Variables - END


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
]

MIDDLEWARE_CLASSES = (
    "djangosecure.middleware.SecurityMiddleware",
)

ROOT_URLCONF = 'helios.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI_APPLICATION = 'helios.wsgi.application'
ASGI_APPLICATION = 'helios.routing.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'HELIOS_POSTGRES_DB',
        'USER': 'HELIOS_POSTGRES_USER',
        'PASSWORD': 'HELIOS_POSTGRES_PASSWORD',
        'HOST': 'HELIOS_POSTGRES_HOST',
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

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Create new vapid key
WEBPUSH_SETTINGS = {
   "VAPID_PUBLIC_KEY": "BI_eye5Ei-Z8_hRLscz_gFRc-1vk1_ZJQ-cygqw-5VWeRrpK1McwDImahkCph0k-ohIdQvvKY3dmpu_6dGigaBM",
   "VAPID_PRIVATE_KEY": "HtAPHFLFV_Wm27g73bFpizHTirz1keQxW1vJ1WrqKv4",
   "VAPID_ADMIN_EMAIL": "support@algonauts.in",
}


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# For Mailing Purpose 
FEEDBACK_EMAIL_USER = 'feedback@gmail.com'
FEEDBACK_EMAIL_PASSWORD = 'algonauts@123'


# For invoice
TAXES = {
    "cgst"  : 9,
    "sgst"  : 9,
    "igst"  : 0,
    "total" : 18
}

GSTIN_NO = "27AARCA7772K1ZV"
PAN_ID = "AARCA7772K"

# Event Hub connect properties
EVENTHUB = False
EVENTHUB_CONNECTION_STRING = "Endpoint=sb://eh-algonautsdev.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=Luh9306fwRWBuS+OA3UFOaVbJKLhWGVEhxQ2P4SMtxU="
EVENTHUB_NAME = "sysadmin"


