from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from users.models import UserGroupMapping, UserGroup, UserGroupType
from django.db.models import query
from django.contrib.auth.decorators import login_required

import datetime
import pytz, re

import users.functions 
import subscriptions.functions 
import subscriptions.constants
from subscriptions.models import Plan, Subscription, OfferPrerequisites, Offer, PlanOfferMap


def plans(request):
    context = {'details' : subscriptions.functions.get_context_for_plans(request.user)}
    # iplans = subscriptions.functions.get_products_in_individual_xxx_plans(1)
    # ipremiumplans = subscriptions.functions.get_products_in_individual_xxx_plans(0)

    # gplans = subscriptions.functions.get_products_in_group_xxx_plans(1)
    # gpremiumplans = subscriptions.functions.get_products_in_group_xxx_plans(0)
    # standard_groups = users.functions.get_all_standard_groups()
    # context = {
    #             'iplans' : iplans,
    #             'ipremiumplans' : ipremiumplans,
    #             'gplans' : gplans,
    #             'gpremiumplans' : gpremiumplans,
    #             'standard_groups' :standard_groups,
    #         }
    # raise EnvironmentError
    return render(request, 'subscriptions/plans.html', context=context)


@login_required(login_url='/accounts/login/')
def individual_one(request): 
    subs_attr = dict(request.POST.lists()) 
    # group_type_name = subs_attr['type_name'][0]
    radio = subs_attr['radio'][0]
    t_delta = subscriptions.constants.PERIOD_ID_DAYS_MAPPING[subs_attr['period'][0]]
    plan_name = subs_attr['radio'][0]

    recepients = []
    if 'group_emails' in subs_attr:    
        email_list = [v.strip() for v in re.split(",", subs_attr['group_emails'][0])]
        recepients.extend(email_list)
    
    subscribe_common(request.user, plan_name, t_delta, payment_id = 0, recepients=recepients)
    return HttpResponseRedirect(redirect_to='/user/profile/info')

@login_required(login_url='/accounts/login/')
def individual_premium(request): 
    subs_attr = dict(request.POST.lists()) 
    # group_type_name = subs_attr['type_name'][0]
    t_delta = subscriptions.constants.PERIOD_ID_DAYS_MAPPING[subs_attr['period'][0]]
    plan_name = subs_attr['radio'][0]

    recepients = []
    if 'group_emails' in subs_attr:    
        email_list = [v.strip() for v in re.split(",", subs_attr['group_emails'][0])]
        recepients.extend(email_list)
    
    subscribe_common(request.user, plan_name, t_delta, payment_id = 0, recepients=recepients)
    return HttpResponseRedirect(redirect_to='/user/profile/info')

@login_required(login_url='/accounts/login/')
def group_one(request): 
    subs_attr = dict(request.POST.lists()) 
    group_type_name = subs_attr['type_name'][0]
    radio = subs_attr['radio'][0]
    t_delta = subscriptions.constants.PERIOD_ID_DAYS_MAPPING[subs_attr['period'][0]]
    plan_name = subs_attr['radio'][0]

    recepients = []
    if 'group_emails' in subs_attr:    
        email_list = [v.strip() for v in re.split(",", subs_attr['group_emails'][0])]
        recepients.extend(email_list)
    
    subscribe_common(request.user, plan_name, t_delta, payment_id = 0, recepients=recepients)
    return HttpResponseRedirect(redirect_to='/user/profile/info')

@login_required(login_url='/accounts/login/')
def group_premium(request): 
    subs_attr = dict(request.POST.lists()) 
    group_type_name = subs_attr['type_name'][0]
    t_delta = subscriptions.constants.PERIOD_ID_DAYS_MAPPING[subs_attr['period'][0]]
    plan_name = subs_attr['radio'][0]

    recepients = []
    if 'group_emails' in subs_attr:    
        email_list = [v.strip() for v in re.split(",", subs_attr['group_emails'][0])]
        recepients.extend(email_list)
    
    subscribe_common(request.user, plan_name, t_delta, payment_id = 0, recepients=recepients)
    pass
    return HttpResponseRedirect(redirect_to='/user/profile/info')

@login_required(login_url='/accounts/login/')
def subscribe(request): 
    subs_attr = dict(request.POST.lists())
    group_type = subs_attr['groupcode'][0]
    plan_type = subs_attr['plancode'][0]
    plan_name = plan_type
    if 'radio' in subs_attr:
        plan_name = subs_attr['radio'][0]
    period = subs_attr['period'][0]
    
    recepients = []
    if 'group_emails' in subs_attr:    
        email_list = [v.strip() for v in re.split(",", subs_attr['group_emails'][0])]
        recepients.extend(email_list)
    
    subscribe_common(user = request.user, group_type = group_type, plan_type= plan_type , plan_name= plan_name, period= period, payment_id = 0, recepients=recepients)

    # raise EnvironmentError
    return HttpResponseRedirect(redirect_to='/user/profile/info')


@login_required(login_url='/accounts/login/') 
def plan_for_users(request):
    iplans, gplans = users.functions.get_user_subs_plans(request.user.id)

#above User must be logged in for selecting a plan
def plan_overview(request, slug):
    now = datetime.datetime.now(pytz.timezone('UTC'))
    plan = Plan.objects.get(plan_name=slug, entry_time__lt = now, expiry_time__gt = now) # get the only active plan
    is_group_plan = subscriptions.functions.is_group_plan(plan_id = plan)
    context = {
                'plan' : plan,
                'is_group_plan' : is_group_plan,
            }
    # raise EnvironmentError
    return render(request, 'subscriptions/plan_overview.html',context=context)

@login_required(login_url='/accounts/login/')
def plan_subscribe(request):
    subs_attr = dict(request.POST.lists()) 
    recepient = [request.user.email]
    if 'group_emails' in subs_attr:    
        email_list = [v.strip() for v in re.split(",", subs_attr['group_emails'][0])]
        recepient.extend(email_list)
        # raise EnvironmentError
    subscribed = Subscription.objects.create_subscription(
                    plan_name = subs_attr['plan_name'][0],
                    user = request.user,
                    group_type = None,
                    period = subs_attr['period'],
                    payment_id = 0,
                )
    if subscribed:
        subscriptions.functions.send_subscription_link(subscribed.user_group_id, recepient)
    return HttpResponseRedirect(redirect_to='/user/profile/info')
    
def subscribe_common(user, group_type, plan_type, plan_name, period, payment_id, recepients = []): 
    recepient = [user.email]
    recepient.extend(recepients)
    subscribed = Subscription.objects.create_subscription(
                    user = user,
                    group_type = group_type,
                    plan_type = plan_type,
                    plan_name = plan_name,
                    period = period,
                    payment_id = payment_id,
                )
    if subscribed:
        subscriptions.functions.send_subscription_link(subscribed.user_group_id, recepients)
    return subscribed





