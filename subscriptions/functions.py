from django.core.mail import send_mass_mail, send_mail
from channels.db import database_sync_to_async

import threading, asyncio, logging
import time, datetime, pytz
from collections.abc import Iterable, Iterator
from users.models import AlgonautsUser, UserGroup, UserGroupType, UserGroupMapping, ReferralOffer, Referral
from subscriptions.models import Plan, Subscription, PlanType, SubscriptionType, Order, Payment
from products.models import Product, ProductCategory, PlanProductMap, ProductFamily
from helios.settings import EMAIL_HOST_USER, client, RAZORPAY_KEY
import users.functions
import jinja2


logger = logging.getLogger("")
loop = asyncio.get_event_loop()


def get_all_plan_type():
    return PlanType.objects.all().order_by('type_name')

def get_plan_id(plan_name, plan_type, group_type):
    """return particular plan id
    
    Arguments:
        plan_name {str} -- plan name
        plan_type {str} -- plan type name
        group_type {str} -- group type name
    """
    group_type = UserGroupType.objects.filter(type_name__iexact = group_type).first()
    plan_type = PlanType.objects.filter(type_name__iexact = plan_type).first()
    return Plan.objects.filter(
                        plan_name = plan_name,
                        user_group_type_id = group_type, 
                        plan_type_id = plan_type
                    ).values("id").first()["id"]

def get_plan_object(plan):
    if isinstance(plan, str):
        return Plan.objects.filter(plan_name__iexact = plan).first()
    if isinstance(plan, int): 
        return Plan.objects.filter(id = plan).first()
    if isinstance(plan, Plan):
        return plan

def get_subscription_type_object(subscription_type, period = True):
    if isinstance(subscription_type, str):
        return SubscriptionType.objects.filter(type_name__iexact = subscription_type).first()
    if isinstance(subscription_type, int):
        if period : return  SubscriptionType.objects.filter(duration_in_days = subscription_type).first()
        return SubscriptionType.objects.filter(id = subscription_type).first()
    if isinstance(subscription_type, SubscriptionType):
        return subscription_type

def get_subscription_type_id(period):
    return SubscriptionType.objects.filter(
                        type_name__iexact = period
                    ).first().values("id")

def get_all_products_in_plan(plan_id:Plan, return_list = False):
    if type(plan_id) == str:
        now = datetime.datetime.now(pytz.timezone('UTC'))
        plan_id = Plan.objects.filter(plan_name = plan_id, entry_time__lt = now, expiry_time__gt = now).last()
    else : plan_id = plan_id if type(plan_id) == Plan else Plan.objects.get(id = plan_id)
    etc = PlanProductMap.objects.filter(plan_id = plan_id).values('product_id')
    if return_list: return list(Product.objects.filter(id__in = etc))
    return Product.objects.filter(id__in = etc)


def get_all_products_in_plans(plans): 
    if not isinstance(plans, Iterable): return get_all_products_in_plans([plans])
    if len(plans) != 0 and type(plans[0]) == Plan:
        plans = [plan.id for plan in plans]
    etc = PlanProductMap.objects.filter(plan_id__in = plans).values('product_id')
    return Product.objects.filter(id__in = etc)


def get_product_family_of_products(products : list):
    if not isinstance(products, Iterable): return get_product_family_of_products([products])
    if len(products) != 0 and type(products[0]) == Product:
            products = [product.id for product in products]
    prod_fam = Product.objects.filter(id__in = products).values('product_family_id')
    return ProductFamily.objects.filter(id__in = prod_fam)


def get_plan_type_of_plans(plans, nobjects = True, preserve_length = False): 
    if not isinstance(plans, Iterable) : return get_plan_type_of_plans([plans])
    if len(plans) != 0 and type(plans[0]) == Plan:
            plans = [plan.id for plan in plans]

    plan_typ = Plan.objects.filter(id__in = plans).values('plan_type_id')
    if preserve_length: plan_typ = [plan_typ.first() for _ in plans]
    if nobjects:
        return [PlanType.objects.get(id = pt['plan_type_id']) for pt in plan_typ]
    return PlanType.objects.filter(id__in = plan_typ)



def get_group_plans():
    now = datetime.datetime.now(pytz.timezone('UTC'))
    enterprize = UserGroupType.objects.exclude(type_name = 'individual') # query give non individual group type
    group_plans = Plan.objects.filter(entry_time__lt = now, expiry_time__gt = now, user_group_type_id__in = enterprize) # query gives active group plans
    return group_plans


def is_group_plan(plan_id):
    plan_id = plan_id if type(plan_id) == int else plan_id.id
    x = get_group_plans().filter(id = plan_id).exists()
    return x


def get_plan(plan_type, plan_name, group_type):
    group_type = UserGroupType.objects.filter(type_name__iexact = group_type)
    if isinstance(plan_type, str):
        plan_type = PlanType.objects.filter(type_name__iexact = plan_type)
    return  Plan.objects.filter(plan_name__iexact = plan_name, user_group_type_id__in = group_type, plan_type_id__in = plan_type).first()

def get_all_plans_from_ids(plans_ids:list, preserve_length = False):
    plans = Plan.objects.filter(id__in = plans_ids)
    if preserve_length: return [plans.first() for _ in plans_ids]
    return plans

def get_all_active_plans():
    now = datetime.datetime.now(pytz.timezone('UTC'))
    return Plan.objects.filter(entry_time__lt = now, expiry_time__gt = now)


def get_all_plans_xxx_type(plan_type:PlanType, exclude = False):
    try:
        if type(plan_type) == str:
            plan_type = PlanType.objects.filter(type_name__iexact = plan_type)[0]
        if type(plan_type) == int:
            plan_type = PlanType.objects.filter(id = plan_type)[0] 
    except IndexError:
        return
    if exclude: return Plan.objects.exclude(plan_type_id = plan_type)
    return Plan.objects.filter(plan_type_id = plan_type)


def get_all_plans_xxx_group(group_type:UserGroupType, exclude = False):
    try:
        if type(group_type) == int:
            group_type = UserGroupType.objects.filter(id = group_type)[0]
        if type(group_type) == str:
            group_type = UserGroupType.objects.filter(type_name__iexact = group_type)[0]
    except IndexError: 
        return
    if exclude :
        return Plan.objects.exclude(user_group_type_id = group_type)
    return Plan.objects.filter(user_group_type_id = group_type)


def get_context_for_plans(user=None):
    user = users.functions.get_user_object(user)
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
            plans = sorted(plans, key = lambda plan: plan.plan_name)
            for k, plan in enumerate(plans):
                plan_id = str(plan.id)
                products = get_all_products_in_plan(plan)
                context[i][0][j][0].append([list(products), plan]) 
    return context


def can_subscribe(user, group_type, plan_type, plan_name):
    # Guy having premium paid subscription should not able to subscribe other non premium plans
    user = users.functions.get_user_object(user)
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
    return not ifsubs or not ifplan 


def is_trial_applicable(group_type, plan_type, plan_name):
    plan_id = Plan.objects.filter(plan_name__iexact = plan_name).order_by('expiry_time').last()
    group_type_id = UserGroupType.objects.filter(type_name = group_type).last()
    plan_type_id = PlanType.objects.filter(type_name = plan_type).last()
    return plan_type_id.trial_applicable and group_type_id.eligible_for_trial 


def already_had_trial(user, group_type, plan_type, plan_name):
    user = users.functions.get_user_object(user)
    plan_id = Plan.objects.filter(plan_name__iexact = plan_name).order_by('expiry_time').last()
    group_type_id = UserGroupType.objects.filter(type_name = group_type).last()
    plan_type_id = PlanType.objects.filter(type_name = plan_type).last()
    if not plan_type_id.trial_applicable or not group_type_id.eligible_for_trial: return True
    user_groups = UserGroupMapping.objects.filter(user_profile_id = user).values("user_group_id")
    user_group_id_ = UserGroup.objects.filter(user_group_type_id = group_type_id, id__in = user_groups)
    user_group_id = user_group_id_.first()
    return Subscription.objects.filter(plan_id = plan_id, user_group_id = user_group_id).exists()
    
    
def send_subscription_link(group, recepients, to = None):
    threading.Thread(target=send_mail_async, args=(group, recepients,)).start()


def get_order_details(group_type, plan_type, plan_name, period):
    return


def send_email(user, recepients, subject, message, to = None):
    if not isinstance(recepients, list) : return send_email(user, [recepients], subject, message) 
    threading.Thread(target=send_mail_async, args=(user, recepients,subject, message)).start()


def send_mail_async(user, recepients, subject, message):
    for to in recepients:
        send_mail(subject, message, EMAIL_HOST_USER, [to], fail_silently=False,)



def register_order(user_group_id, razorpay_order):
    Order.objects.create(
        user_group_id = user_group_id,
        order_amount = razorpay_order['amount'],
        order_currency = razorpay_order['currency'],
        order_receipt = razorpay_order['receipt'],
        notes = str(razorpay_order['notes']),
        razorpay_order_id = razorpay_order['id'],
        razorpay_payment_id = "---"
    )


def register_payment(order_id, payment_id, signature, invoice_id):
    if type(order_id) == str:
        order_id = get_order_instance(order_id)
    if not order_id : return None
    payment = Payment.objects.create(
        payment_ref = payment_id,
        order_id = order_id,
        user_group_id = order_id.user_group_id,
        signature = signature,
        amount = order_id.order_amount,    
        invoice_id = invoice_id
    )
    Order.objects.filter(razorpay_order_id = order_id.razorpay_order_id).update(razorpay_payment_id = payment_id)
    return payment

def end_subscription(user, plan, subscription_type):
    user_group_id = users.functions.get_user_group(user, plan.user_group_type_id)
    subscription = Subscription.objects.filter(
        user_group_id = user_group_id,
        plan_id = plan,
        subscription_type_id = subscription_type
    )
    subscription.update(
        subscription_end = datetime.datetime.now(pytz.timezone('UTC')),
        subscription_active = False
    )

def get_order_instance(order_id):
    return Order.objects.get(razorpay_order_id = order_id)
 
def create_subscription(user, group_type, plan_type, plan_name, period, payment_id):
    subscribed = Subscription.objects.create_subscription(
                    user = user,
                    group_type = group_type,
                    plan_type = plan_type,
                    plan_name = plan_name,
                    period = period,
                    payment_id = payment_id,
                )
    return subscribed

def get_all_subscriptions_of_user(user):
    user = users.functions.get_user_object(user)
    now = datetime.datetime.now(pytz.timezone('UTC'))

    user_all_groups = UserGroupMapping.objects.filter(
                            user_profile_id = user, 
                            time_removed__gt = datetime.datetime.now(pytz.timezone('UTC'))
                            ).values(
                                'user_profile_id', 
                                'user_group_id', 
                                'user_group_id__user_group_type_id'
                                ).values('user_group_id') # one user linked with multiple groups

    return Subscription.objects.filter(
                            user_group_id__in = user_all_groups, 
                            subscription_end__gt = now, 
                            subscription_start__lt = now)

def get_subscriptions_from_invoice_id(invoice_id):
    return Subscription.objects.filter(payment_id__invoice_id = invoice_id).first()