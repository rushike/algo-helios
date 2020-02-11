from django.core.mail import send_mass_mail, send_mail
import threading
import time, datetime, pytz
from users.models import AlgonautsUser, UserGroup, UserGroupType, UserGroupMapping, ReferralOffer, Referral
from subscriptions.models import Plan, Subscription, PlanType
from products.models import Product, ProductCategory, PlanProductMap
from helios.settings import EMAIL_HOST_USER, ABSOLUTE_URL_HOME
import users.functions

def get_all_plan_type():
    return PlanType.objects.all()

def get_all_products_in_plan(plan_id:Plan):
    plan_id = plan_id if type(plan_id) == Plan else Plan.objects.get(id = plan_id)
    etc = PlanProductMap.objects.filter(plan_id = plan_id).values('product_id')
    return Product.objects.filter(id__in = etc)

def get_group_plans():
    now = datetime.datetime.now()
    enterprize = UserGroupType.objects.exclude(type_name = 'individual') # query give non individual group type
    group_plans = Plan.objects.filter(entry_time__lt = now, expiry_time__gt = now, user_group_type_id__in = enterprize) # query gives active group plans
    return group_plans

def is_group_plan(plan_id):
    plan_id = plan_id if type(plan_id) == int else plan_id.id
    x = get_group_plans().filter(id = plan_id).exists()
    return x

def get_individual_plans():
    now = datetime.datetime.now()
    individual = UserGroupType.objects.filter(type_name = 'individual') # query give non individual group type
    indv_plans = Plan.objects.filter(entry_time__lt = now, expiry_time__gt = now, user_group_type_id__in = individual, plan_name__startswith = 'i_') # query gives active group plans
    return indv_plans

def get_products_in_individual_xxx_plans(typeof):
    if typeof is None:
        iplans = get_individual_plans()
        products = list()
        for plan in iplans:
            prod = (get_all_products_in_plan(plan))
            products.extend(prod)
        return products
    elif typeof == 1:
        iplans  = get_individual_plans()
        iplans = iplans.exclude(plan_name = 'i_Premium')
        products = list()
        for plan in iplans:
            prod = (get_all_products_in_plan(plan))
            products.extend(prod)
        return products
    else : 
        iplans  = get_individual_plans()
        iplan = iplans.filter(plan_name = 'i_Premium').order_by('-expiry_time')[0]
        products = list(get_all_products_in_plan(iplan))
        return products

def get_products_in_group_xxx_plans(typeof):
    if typeof is None:
        iplans = get_group_plans()
        products = list()
        for plan in iplans:
            prod = (get_all_products_in_plan(plan))
            products.extend(prod)
        return products
    elif typeof == 1:
        iplans  = get_group_plans()
        iplans = iplans.exclude(plan_name = 'g_Premium')
        products = list()
        for plan in iplans:
            prod = (get_all_products_in_plan(plan))
            products.extend(prod)
        return products
    else : 
        iplans  = get_group_plans()
        iplan = iplans.filter(plan_name = 'g_Premium').order_by('-expiry_time')[0]
        products = list(get_all_products_in_plan(iplan))
        return products

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

def get_context_for_plans2(user=None):
    context = {}
    plan_types = get_all_plan_type()
    user_groups = users.functions.get_all_standard_groups()
    for group_type in user_groups:
        plan_group_id = str(group_type).lower()
        context[plan_group_id] = [{}, group_type]
        for plan_type in plan_types:
            plan_type_id = str(plan_type).lower()
            context[plan_group_id][0][plan_type_id] = [{}, plan_type]
            plans = Plan.objects.filter(plan_type_id = plan_type, user_group_type_id = group_type)
            for plan in plans:
                plan_id = str(plan.id)
                products = get_all_products_in_plan(plan)
                context[plan_group_id][0][plan_type_id][0][plan_id] = [list(products), plan]
                pass 
    return context

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

def send_subscription_link(group, recepients, to = None):
    threading.Thread(target=send_mail_async, args=(group, recepients,)).start()

def send_mail_async(group, recepients,):
    if not isinstance(recepients, list) : return send_subscription_link(group, [recepients]) 
    start = time.time()
    subject = 'Algonauts Plan Subscription Link'
    message = 'This is the link for subscription for group : ' + ABSOLUTE_URL_HOME + users.functions.generate_group_add_link(group)
    for to in recepients:
        send_mail(subject, message, EMAIL_HOST_USER, [to], fail_silently=False,)
    return  
