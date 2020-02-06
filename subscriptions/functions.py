from users.models import AlgonautsUser, UserGroup, UserGroupType, UserGroupMapping, ReferralOffer, Referral
from subscriptions.models import Plan, Subscription
from products.models import Product, ProductCategory, PlanProductMap
from django.core.mail import send_mass_mail, send_mail
import threading
import users.functions
import time, datetime
from helios.settings import EMAIL_HOST_USER, ABSOLUTE_URL_HOME


def get_all_products_in_plan(plan_id:Plan):
    plan_id = plan_id if type(plan_id) == Plan else Plan.objects.get(id = plan_id)
    etc = PlanProductMap.objects.filter(plan_id = plan_id)
    print(etc)

def get_group_plan():
    now = datetime.datetime.now()
    enterprize = UserGroupType.objects.exclude(type_name = 'individual') # query give non individual group type
    group_plan = Plan.objects.filter(entry_time__lt = now, expiry_time__gt = now, user_group_type_id__in = enterprize) # query gives active group plans
    return group_plan

def create_premium_plan(sender, instance, **kwargs):
    now = datetime.datetime.now()
    ipremium_plan = Plan.objects.get_(plan_name= 'ipremium', entry_time__lt = now, expiry_time__gt = now) # get the ipremium
    get_all_products = Product.objects.all()
    for product in get_all_products:
        PlanProductMap.objects.get_or_create(plan_id = ipremium_plan, product_id = product)
        pass
    pass

def is_group_plan(plan_id):
    plan_id = plan_id if type(plan_id) == int else plan_id.id
    x = get_group_plan().filter(id = plan_id).exists()
    return x

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
