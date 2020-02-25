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
CRONJOBS = [
    ('0 0 * * *', 'subscriptions.cron.check_data_consistency')
]