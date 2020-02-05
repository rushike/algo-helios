from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from users.models import UserGroupMapping, UserGroup, UserGroupType
from django.db.models import query
from django.contrib.auth.decorators import login_required

import datetime
import pytz

import users.functions 
import subscriptions.functions 
from subscriptions.models import Plan, Subscription, OfferPrerequisites, Offer, PlanOfferMap


def plans(request):
    context = {
                'iplans' : Plan.objects.filter(plan_name__startswith = 'i_'),
                'gplans' : Plan.objects.exclude(plan_name__startswith = 'i_')
            }
    # raise EnvironmentError
    return render(request, 'subscriptions/plans.html', context=context)

@login_required(login_url='/accounts/login/') 
#above User must be logged in for selecting a plan
def plan_overview(request, slug):
    iplans, gplans = users.functions.get_user_subs_plans(request.user.id)
    context = {
                'iplans' : iplans, 
                'gplans' : gplans,
                'plan' : Plan.objects.get(plan_name=slug)
            }
    
    return render(request, 'subscriptions/plan_overview.html',context=context)

@login_required(login_url='/accounts/login/')
def plan_subscribe(request):
    subs_attr = dict(request.POST.lists()) 
    recepient = [request.user.email]
    recepient.extend(subs_attr['group_emails'])
    subscribed = Subscription.objects.create_subscription(
                    plan_name = subs_attr['plan_name'][0],
                    user = request.user,
                    t_delta = int(subs_attr['t_delta'][0]),
                    payment_id = 0,
                )
    if subscribed:
        subscriptions.functions.send_subscription_link(subscribed.user_group_id, recepient)
    return HttpResponseRedirect(redirect_to='/user/profile/info')
    




