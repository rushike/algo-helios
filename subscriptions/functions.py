from users.models import AlgonautsUser, UserGroup, UserGroupType, UserGroupMapping, ReferralOffer, Referral
from subscriptions.models import Plan, Subscription
from products.models import Product, ProductCategory, PlanProductMap
from django.core.mail import send_mass_mail, send_mail
import threading
import users.functions
import time
from helios.settings import EMAIL_HOST_USER, ABSOLUTE_URL_HOME


def get_all_products_in_plan(plan_id:Plan):
    plan_id = plan_id if type(plan_id) == Plan else Plan.objects.get(id = plan_id)
    etc = PlanProductMap.objects.filter(plan_id = plan_id)
    print(etc)
    # raise EnvironmentError

def send_subscription_link(group, recepients, to = None):
    threading.Thread(target=send_mail_async, args=(group, recepients,)).start()

def send_mail_async(group, recepients,):
    if not isinstance(recepients, list) : return send_subscription_link(group, [recepients]) 
    start = time.time()
    subject = 'Algonauts Plan Subscription Link'
    message = 'This is the link for subscription for group : ' + ABSOLUTE_URL_HOME + users.functions.generate_group_add_link(group)
    # datagram = (subject, message, EMAIL_HOST_USER, recepients)
    for to in recepients:
        send_mail(subject, message, EMAIL_HOST_USER, [to], fail_silently=False,)
    return  