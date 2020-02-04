from users.models import AlgonautsUser, UserGroup, UserGroupType, UserGroupMapping, ReferralOffer, Referral
from subscriptions.models import Plan, Subscription
from products.models import Product, ProductCategory, PlanProductMap
from django.core.mail import send_mass_mail

import users.functions
from helios.settings import EMAIL_HOST_USER, ABSOLUTE_URL_HOME

def send_subscription_link(group, recepients):
    if not isinstance(recepients, list) : return send_subscription_link(group, [recepients]) 
    subject = 'Algonauts Plan Subscription Link'
    message = 'This is the link for subscription for group : ' + ABSOLUTE_URL_HOME + users.functions.generate_group_add_link(group)
    datagram = (subject, message, EMAIL_HOST_USER, recepients)
    send_mass_mail(datagram, fail_silently = False)