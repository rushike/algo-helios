from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from users.models import UserGroupMapping, UserGroup, UserGroupType
from django.db.models import query
from django.contrib.auth.decorators import login_required
import datetime, pytz, re
import users.functions 
import subscriptions.functions 
from subscriptions.models import Plan, Subscription, OfferPrerequisites, Offer, PlanOfferMap

def plans(request):
    context = {'details' : subscriptions.functions.get_context_for_plans(request.user)}
    return render(request, 'subscriptions/plans.html', context=context)

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
    
    subscribe_common(user = request.user, group_type = group_type, plan_type= plan_type , \
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
    subs_attr = dict(request.POST.lists()) 
    recepient = [request.user.email]
    if 'group_emails' in subs_attr:    
        email_list = [v.strip() for v in re.split(",", subs_attr['group_emails'][0])]
        recepient.extend(email_list)
    subscribed = Subscription.objects.create_subscription(
                    plan_name = subs_attr['plan_name'][0],
                    user = request.user,
                    group_type = None,
                    period = subs_attr['period'],
                    payment_id = 0,
                )
    if subscribed:
        subject = 'Algonauts Plan Subscription Link'
        message = 'This is the link for subscription for group : ' + ABSOLUTE_URL_HOME + users.functions.generate_group_add_link(group)
        subscriptions.functions.send_email(subscribed.user_group_id, recepient, subject, message)
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
        subscriptions.functions.send_email(subscribed.user_group_id, recepients)
    return subscribed





