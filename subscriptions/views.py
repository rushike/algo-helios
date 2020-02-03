from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from users.models import UserGroupMapping, UserGroup, UserGroupType
from django.db.models import query
from subscriptions.models import Plan, Subscription, OfferPrerequisites, Offer, PlanOfferMap
import datetime
from django.contrib.auth.decorators import login_required
import pytz
from users.functions import *


def plans(request):
    return render(request, 'subscriptions/plans.html', {'plans' : Plan.objects.filter(is_active=True) })

@login_required(login_url='/accounts/login/') 
#above User must be logged in for selecting a plan
def plan_overview(request, slug):
    iplans, gplans = get_user_subs_plans(request.user.id)
    context = {
                'iplans' : iplans, 
                'gplans' : gplans,
                'plan' : Plan.objects.get(plan_name=slug)
            }
    
    return render(request, 'subscriptions/plan_overview.html',context=context)


def plan_subscribe(request):
    subs_attr = dict(request.POST.lists()) 
    Subscription.objects.create_subscription(
        plan_name = subs_attr['plan_name'][0],
        user = request.user,
        t_delta = int(subs_attr['t_delta'][0]),
        payment_id = 0,
    )
    # raise AttributeError
    # return HttpResponse(u_g) #shows User linked to Exact Group & Group Type
    return HttpResponseRedirect(redirect_to='/user/profile/info')
    




