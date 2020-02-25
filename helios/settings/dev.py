from .common import *
from razorpay import Client

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
    'dev.algonauts.in',
    'algonauts.in',
]

"""
Local database credentials
"""
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

"""
cronjobs timeing adjustment
"""
CRONJOBS = [
    ('*/1 * * * *', 'subscriptions.cron.check_data_consistency')
]

