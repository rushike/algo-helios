from django.core.mail import send_mass_mail, send_mail
import threading
import time, datetime, pytz
from users.models import AlgonautsUser, UserGroup, UserGroupType, UserGroupMapping, ReferralOffer, Referral
from subscriptions.models import Plan, Subscription, PlanType, SubscriptionType
from products.models import Product, ProductCategory, PlanProductMap
from helios.settings import EMAIL_HOST_USER, ABSOLUTE_URL_HOME
import users.functions
import jinja2

def get_all_plan_type():
    return PlanType.objects.all().order_by('type_name')

def get_all_products_in_plan(plan_id:Plan):
    plan_id = plan_id if type(plan_id) == Plan else Plan.objects.get(id = plan_id)
    etc = PlanProductMap.objects.filter(plan_id = plan_id).values('product_id')
    return Product.objects.filter(id__in = etc)

def get_group_plans():
    now = datetime.datetime.now(pytz.timezone('UTC'))
    enterprize = UserGroupType.objects.exclude(type_name = 'individual') # query give non individual group type
    group_plans = Plan.objects.filter(entry_time__lt = now, expiry_time__gt = now, user_group_type_id__in = enterprize) # query gives active group plans
    return group_plans

def is_group_plan(plan_id):
    plan_id = plan_id if type(plan_id) == int else plan_id.id
    x = get_group_plans().filter(id = plan_id).exists()
    return x

def get_all_plans_xxx_type(plan_type:PlanType):
    try:
        if type(plan_type) == str:
            plan_type = PlanType.objects.filter(type_name = plan_type)[0]
        if type(plan_type) == int:
            plan_type = PlanType.objects.filter(id = plan_type)[0] 
    except IndexError:
        return
    return Plan.objects.filter(plan_type_id = plan_type)

def get_all_plans_xxx_group(group_type:UserGroupType):
    try:
        if type(group_type) == int:
            group_type = UserGroupType.objects.filter(id = group_type)[0]
        if type(group_type) == str:
            group_type = UserGroupType.objects.filter(type_name = group_type)[0]
    except IndexError: 
        return
    return Plan.objects.filter(user_group_type_id = group_type)

def get_context_for_plans(user=None):
    context = []
    plan_types = get_all_plan_type()
    user_groups = users.functions.get_all_standard_groups()
    for i, group_type in enumerate(user_groups):
        plan_group_id = str(group_type).lower()
        context.append([[], group_type])
        for j, plan_type in enumerate(plan_types):
            plan_type_id = str(plan_type).lower()
            context[i][0].append([[], plan_type])
            plans = Plan.objects.filter(plan_type_id = plan_type, user_group_type_id = group_type)  
            for k, plan in enumerate(plans):
                plan_id = str(plan.id)
                products = get_all_products_in_plan(plan)
                context[i][0][j][0].append([list(products), plan])
                pass 
    return context

def can_subscribe(user, group_type, plan_type, plan_name):
    # Guy having premium paid subscription should not able to subscribe other non premium plans
    plan_id = Plan.objects.filter(plan_name__iexact = plan_name).order_by('expiry_time').last()
    group_type_id = UserGroupType.objects.filter(type_name = group_type).last()
    plan_type_id = PlanType.objects.filter(type_name = plan_type).last()
    user_groups = UserGroupMapping.objects.filter(user_profile_id = user).values("user_group_id")
    user_group_id = UserGroup.objects.filter(user_group_type_id = group_type_id, id__in = user_groups).first()
    non_trial_subs = SubscriptionType.objects.exclude(type_name__iexact = 'Trial')
    premium_plan_type = PlanType.objects.get(type_name__iexact = 'Premium')
    subs_plans = Subscription.objects.filter(user_group_id = user_group_id, subscription_type_id__in = non_trial_subs).values('plan_id')
    ifsubs = subs_plans.exists()
    ifplan = Plan.objects.filter(id__in = subs_plans, plan_type_id = premium_plan_type).exists()
    ret = not ifsubs or not ifplan 
       
    return ret

def is_trial_applicable(group_type, plan_type, plan_name):
    plan_id = Plan.objects.filter(plan_name__iexact = plan_name).order_by('expiry_time').last()
    group_type_id = UserGroupType.objects.filter(type_name = group_type).last()
    plan_type_id = PlanType.objects.filter(type_name = plan_type).last()
    return plan_type_id.trial_applicable and group_type_id.eligible_for_trial 

def already_had_trial(user, group_type, plan_type, plan_name):
    plan_id = Plan.objects.filter(plan_name__iexact = plan_name).order_by('expiry_time').last()
    group_type_id = UserGroupType.objects.filter(type_name = group_type).last()
    plan_type_id = PlanType.objects.filter(type_name = plan_type).last()
    if not plan_type_id.trial_applicable or not group_type_id.eligible_for_trial: return True
    user_groups = UserGroupMapping.objects.filter(user_profile_id = user).values("user_group_id")
    user_group_id_ = UserGroup.objects.filter(user_group_type_id = group_type_id, id__in = user_groups)
    user_group_id = user_group_id_.first()
    etz = Subscription.objects.filter(plan_id = plan_id, user_group_id = user_group_id).exists()
    # raise EnvironmentError
    return etz
    
def send_subscription_link(group, recepients, to = None):
    threading.Thread(target=send_mail_async, args=(group, recepients,)).start()
    
def send_email(group, recepients, subject, message, to = None):
    threading.Thread(target=send_mail_async, args=(group, recepients,subject, message)).start()

def send_mail_async(group, recepients, subject, message):
    if not isinstance(recepients, list) : return send_email(group, [recepients]) 
    start = time.time()
    for to in recepients:
        send_mail(subject, message, EMAIL_HOST_USER, [to], fail_silently=False,)