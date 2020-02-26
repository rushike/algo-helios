from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.db.models import query
from django.contrib.auth.decorators import login_required

import datetime, pytz, re
from razorpay.errors import SignatureVerificationError

import users.functions 
from helios.settings import EMAIL_HOST_USER, client, RAZORPAY_KEY
import subscriptions.functions 
from subscriptions.models import Plan, Subscription, OfferPrerequisites, Offer, PlanOfferMap
from users.models import UserGroupMapping, UserGroup, UserGroupType



def plans(request):
    POST = request.session.get('order_details_post')
    if 'order_details_post' in request.session: del request.session['order_details_post']
    alert = POST.get('alert')  if POST else False
    context = {'details' : subscriptions.functions.get_context_for_plans(request.user), 'alert' : alert}
    return render(request, 'subscriptions/plans.html', context=context)

@login_required(login_url='/accounts/login/')
def neft_details(request):
    POST = dict(request.POST.lists())
    if not POST: 
        POST = request.session.get('order_details_post')
        if 'order_details_post' in request.session: del request.session['order_details_post']
    plan = subscriptions.functions.get_plan(POST['plan_type'], POST['plan_name'], POST['group_type'])
    POST["amount"] = plan.price_per_month if POST['period'].lower() == 'monthly' else plan.price_per_year

    request.session['order_details_post'] = POST
    context = {'order_details' : POST, }

    return render(request, 'subscriptions/neft_details.html', context=context)

@login_required(login_url="/account/login/")
def send_neft_details(request):
    POST = request.session.get('order_details_post')
    post = dict(request.POST.lists())
    payment_ref = post['payment-ref'][0]   
    if 'order_details_post' in request.session: del request.session['order_details_post']
    recepient = [EMAIL_HOST_USER]
    subject = "Get the plan"
    mail_body  = "'Name : " + request.user.first_name + " " + request.user.last_name + "\n" +\
                "Email : " + request.user.email+ "\n" +\
                "Plan Name : " + POST['plan_name'] + " Period :  " + POST['period'].title() +"\n" +\
                "Billing Amount : " + str(POST['amount']) +"\n" +\
                "Payment Reference : '" + str(payment_ref)

    subscriptions.functions.send_email(request.user.email, recepient, subject, mail_body)
    return HttpResponseRedirect(redirect_to=  "/user/profile/info")


def order_details(request):
    subs_attr1 = dict(request.GET.lists())
    POST = dict(request.POST.lists())
    group_type = POST['groupcode'][0]
    plan_type = POST['plancode'][0]
    plan_name = POST['planname'][0]
    if 'plan_name' in POST:
        plan_name = POST['plan_name'][0]
    period = POST['period'][0]
    
    POST = {
        'group_type' : group_type,
        'plan_type' : plan_type,
        'plan_name' : plan_name,
        'period' : period,
        'alert' : False
    }    
    request.session['order_details_post'] = POST
    return HttpResponseRedirect("/subscriptions/orders")

@login_required(login_url='/subscriptions/plans')
def create_order(request):
    POST = request.session.get('order_details_post')
    amount = POST.get('amount')
    plan_name = POST.get('plan_name')
    group_type = POST.get('group_type')
    plan_type = POST.get('plan_type')
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'
    notes = {'plan_name': plan_name, 'plan_type' : plan_type, 'group_type' : group_type}   # OPTIONALclient.order.create(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0')
    amount = amount if amount != 0 else 10000
    DATA = {
                "amount" : amount,
                "currency" : order_currency,
                "receipt" : order_receipt,
                "notes" : notes,
                "payment_capture" : 0
            }

    order = client.order.create(data = DATA)
    user_group_id = users.functions.get_group_of_user(request.user, plan_name)
    subscriptions.functions.register_order(user_group_id = user_group_id, razorpay_order = order)
    context = {
        "order_id" : order["id"],
        "amount" : amount,
        "currency" : order_currency,
        "plan_details" : "|".join([plan_type, '-'.join(plan_name.split()), group_type]),
        "name" : " ".join([request.user.first_name, request.user.last_name]),
        'email' : request.user.email,
        'contact' : request.user.contact_no,
        'razorpay_key' : RAZORPAY_KEY
    }
    return render(request, 'subscriptions/payment.html', context = context)
    # return HttpResponse("Your order is " + str(order))

def payment_success(request):
    POST = request.session.get('order_details_post')
    verifying_dict = {
        'razorpay_order_id' : request.POST.get('razorpay_order_id'),
        'razorpay_payment_id' : request.POST.get('razorpay_payment_id'),
        'razorpay_signature' : request.POST.get('razorpay_signature'),
    }
    try :
        client.utility.verify_payment_signature(verifying_dict)
    except SignatureVerificationError:
        #payment not verified sucessfully
        return HttpResponseRedirect(redirect_to="/subscriptions/plans")
    request.session['order_details_post'] = POST
    request.session['order_details_post'].update({'order_id' : request.POST.get('razorpay_order_id'), 'payment_id' : request.POST.get('razorpay_payment_id'),})
    
    return HttpResponseRedirect('/subscriptions/subscribe')

@login_required(login_url='/accounts/login/')
def secure_order_details(request):
    POST = request.session.get('order_details_post')
    group_type, plan_type, plan_name = POST['group_type'], POST['plan_type'], POST['plan_name']
    if not subscriptions.functions.can_subscribe(request.user, group_type, plan_type, plan_name):
        POST["alert"] = True
        request.session['order_details_post'] = POST
        return HttpResponseRedirect(redirect_to='/subscriptions/plans')
    if subscriptions.functions.is_trial_applicable(group_type = group_type, plan_type = plan_type, plan_name = plan_type):
        request.session['order_details_post'] = POST
        if not subscriptions.functions.already_had_trial(request.user, group_type, plan_type, plan_name):
            return HttpResponseRedirect(redirect_to = "/subscriptions/subscribe")
    request.session['order_details_post'] = POST
    return HttpResponseRedirect(redirect_to = '/subscriptions/neft-details')

@login_required(login_url='/accounts/login/')
def subscribe(request): 
    subs_attr = dict(request.POST.lists())
    POST = request.session.get('order_details_post')

    if not POST : return HttpResponseRedirect(redirect_to='/subscriptions/plans')

    if 'order_details_post' in request.session: del request.session['order_details_post']
    group_type = POST['group_type']
    plan_type = POST['plan_type']
    plan_name = POST['plan_name']
    
    period = POST['period']

    order_id = POST.get('order_id')
    payment_id = POST.get('payment_id')
    
    recepients = []
    if 'group_emails' in POST:    
        email_list = [v.strip() for v in re.split(",", POST['group_emails'][0])]
        recepients.extend(email_list)
    
    subscription_id = subscribe_common(user = request.user, group_type = group_type, plan_type= plan_type ,   \
                    plan_name= plan_name, period= period, payment_id = 0, recepients=recepients)
    subscriptions.functions.register_payment(order_id, payment_id,subscription_id)
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
                    plan_type = POST['plan_type'],
                    group_type = None,
                    period = POST['period'],
                    payment_id = 0,
                )
    group = users.functions.get_group_of_user(request.user, POST['plan_name'])
    if subscribed:
        subject = 'Algonauts Plan Subscription Link'
        message = 'This is the link for subscription for group : ' + request.build_absolute_uri(users.functions.generate_group_add_link(group))
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
        subject = "Regarding Algonauts Subscription"
        message = "You have successfully subscribed to algonauts plan : " + str(plan_name)
        subscriptions.functions.send_email(user, recepients, subject, message)
    return subscribed
