from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from users.models import UserGroupMapping, UserGroup, UserGroupType
from django.db.models import query
from django.contrib.auth.decorators import login_required
import datetime
import pytz, re
import users.functions 
import subscriptions.functions 
from subscriptions.models import Plan, Subscription, OfferPrerequisites, Offer, PlanOfferMap

def plans(request):
    POST = request.session.get('order_details_post')
    if 'order_details_post' in request.session: del request.session['order_details_post']
    alert = POST['alert']  if POST else False
    context = {'details' : subscriptions.functions.get_context_for_plans(request.user), 'alert' : alert}
    return render(request, 'subscriptions/plans.html', context=context)

@login_required(login_url='/accounts/login/')
def order_details(request):
    subs_attr1 = dict(request.GET.lists())
    POST = dict(request.POST.lists())
    # POST = dict(request.POST.lists())
    group_type = POST['groupcode'][0]
    plan_type = POST['plancode'][0]
    plan_name = plan_type
    if 'radio' in POST:
        plan_name = POST['radio'][0]
    period = POST['period'][0]

    POST = {
        'group_type' : group_type,
        'plan_type' : plan_type,
        'plan_name' : plan_name,
        'period' : period,
        'alert' : False
    }

    if not subscriptions.functions.can_subscribe(request.user, group_type, plan_type, plan_name):
        POST["alert"] = True
        request.session['order_details_post'] = POST
        return HttpResponseRedirect(redirect_to='/subscriptions/plans')
    if subscriptions.functions.is_trial_applicable(group_type = group_type, plan_type = plan_type, plan_name = plan_type):
        request.session['order_details_post'] = POST
        if not subscriptions.functions.already_had_trial(request.user, group_type, plan_type, plan_name):
            # request.session['order_details_post'] = request.POST
            raise EnvironmentError
            return HttpResponseRedirect(redirect_to = "/subscriptions/subscribe")
        # return HttpResponseRedirect(redirect_to = "/subscriptions/subscribe")
    
    
    request.session['order_details_post'] = POST
    # raise EnvironmentError
    return render(request, 'subscriptions/order_details.html', context=POST)

@login_required(login_url='/accounts/login/')
def subscribe(request): 
    subs_attr = dict(request.POST.lists())
    POST = request.session.get('order_details_post')
    if not POST : return 

    if 'order_details_post' in request.session: del request.session['order_details_post']
    group_type = POST['group_type']
    plan_type = POST['plan_type']
    plan_name = POST['plan_name']
    
    period = POST['period']
    
    recepients = []
    if 'group_emails' in POST:    
        email_list = [v.strip() for v in re.split(",", POST['group_emails'][0])]
        recepients.extend(email_list)
    
    subscribe_common(user = request.user, group_type = group_type, plan_type= plan_type ,   \
                    plan_name= plan_name, period= period, payment_id = 0, recepients=recepients)
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
    return render(request, 'subscriptions/plan_overview.html',context=context)

@login_required(login_url='/accounts/login/')
def plan_subscribe(request):
    POST = dict(request.POST.lists()) 

    recepient = [request.user.email]
    if 'group_emails' in POST:    
        email_list = [v.strip() for v in re.split(",", POST['group_emails'][0])]
        recepient.extend(email_list)
    subscribed = Subscription.objects.create_subscription(
                    plan_name = POST['plan_name'][0],
                    user = request.user,
                    group_type = None,
                    period = POST['period'],
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





