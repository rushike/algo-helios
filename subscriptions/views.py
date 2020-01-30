from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from users.models import UserGroupMapping, UserGroup, UserGroupType
from django.db.models import query
from subscriptions.models import Plan, Subscription, OfferPrerequisites, Offer, PlanOfferMap
import datetime
from django.contrib.auth.decorators import login_required
import pytz

def plans(request):
    return render(request, 'subscriptions/plans.html', {'plans' : Plan.objects.all()})

@login_required(login_url='/accounts/login/') 
#above User must be logged in for selecting a plan
def plan_overview(request, slug):
    return render(request, 'subscriptions/plan_overview.html', {'plan' : Plan.objects.get(plan_name=slug)})


def plan_subscribe(request):
    subs_attr = dict(request.POST.lists()) 
    subs_attr['email'] = request.user.email #get users email
    ru = request.user
    # user_plan is an array type
    user_plan = Plan.objects.filter(plan_name=subs_attr['plan_name'][0])[0] 

    #one user linked with multiple groups
    
    ne = UserGroup.objects.create_user_group(user_plan.user_group_type_id, datetime.datetime.now(), admin=request.user)
    ugti = user_plan.user_group_type_id.id
    usermpa = UserGroupMapping.objects.all()
    u_gid = UserGroupMapping.objects.all().values('user_group_id','user_profile_id','user_group_id__user_group_type_id') \
        .filter(user_profile_id=request.user, user_group_id__user_group_type_id=user_plan.user_group_type_id)
    
    now = datetime.datetime.now(pytz.timezone('UTC'))
    # now = datetime.datetime.strftime(now, "%Y-%m-%d")
    u_g = UserGroup.objects.get(id=u_gid[0]['user_group_id'])
    # all_off = Offer.objects.all().values('offer_start_date','offer_end_date').filter(offer_end_date__gt = now, offer_start_date__lt = now)
    live_offer_id = PlanOfferMap.objects.all().values('offer_id','plan_id','offer_id__offer_start_date','offer_id__offer_end_date') \
        .filter(offer_id__offer_end_date__gt = now, offer_id__offer_start_date__lt = now)
    
    live_offer_id = live_offer_id[0]['offer_id']
    # dat = all_off['offer_end_date']
    # subs_all = Subscription.objects.all().values('offer_id')
    live_offer_id = Offer.objects.get(id=live_offer_id)    
    # current_plan_id = Plan.

    Subscription.objects.create(
        user_group_id = u_g,
        plan_id = user_plan,
        offer_id = live_offer_id,
        subscription_start = datetime.datetime.now(),
        subscription_end = datetime.datetime.now() + datetime.timedelta(days=1),
        subscription_active = True,
        payment_id = 0, 
    ).save()
    # raise AttributeError
    # return HttpResponse(u_g) #shows User linked to Exact Group & Group Type
    return HttpResponseRedirect(redirect_to='/user/profile/'+str(request.user.id))
    




