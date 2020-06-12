from django.shortcuts import render, HttpResponse, HttpResponseRedirect     
from django.http import JsonResponse
from django.db.models import query
from django.contrib.auth.decorators import login_required

import requests
import datetime, pytz, re, logging
from razorpay.errors import SignatureVerificationError
import wkhtmltopdf
from wkhtmltopdf.views import PDFTemplateView

import users.functions 
from helios.settings import EMAIL_HOST_USER, client, RAZORPAY_KEY

import subscriptions.functions 
import subscriptions.razorpay
from subscriptions.models import Plan, Subscription, OfferPrerequisites, Offer, PlanOfferMap
from users.models import UserGroupMapping, UserGroup, UserGroupType


logger = logging.getLogger('normal')


def plans(request):
    POST = request.session.get('order_details_post')
    if 'order_details_post' in request.session: del request.session['order_details_post']
    alert = POST.get('alert')  if POST else False
    context = {'details' : subscriptions.functions.get_context_for_plans(request.user), 'alert' : alert}
    return render(request, 'subscriptions/plans.html', context=context)


def plans2(request):
    POST = request.session.get('order_details_post')
    if 'order_details_post' in request.session: del request.session['order_details_post']
    alert = POST.get('alert')  if POST else False
    context = {'details' : subscriptions.functions.get_context_for_plans2(request.user), 'alert' : alert}
    return render(request, 'subscriptions/plans_copy.html', context=context)


def mercury_product_data(request):
    data = subscriptions.functions.get_context_for_plans2(request.user)
    return JsonResponse(data, safe=False)

def can_subscribe(request):
    pass

@login_required(login_url='/accounts/login/')
def neft_details(request):
    POST = dict(request.POST.lists())
    if not POST: 
        POST = request.session.get('order_details_post')
        # if 'order_details_post' in request.session: del request.session['order_details_post']
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


def plan_data(request):
    group_type = request.POST.get('groupcode')
    plan_type = request.POST.get('plancode')
    plan_name = request.POST.get('planname')
    if 'plan_name' in request.POST:
        plan_name = request.POST.get('plan_name')
    period = request.POST.get('period', 'monthly')
    plan = subscriptions.functions.get_plan(plan_type, plan_name, group_type)
    amount = plan.price_per_month if period.lower() == 'monthly' else plan.price_per_year
    gst = .18 * amount
    total_amount = 1.18 * amount
    context = {
        'group_type' : group_type,
        'group_max_members' : users.functions.get_max_members_in_group(group_type),
        'plan_type' : plan_type,
        'plan_name' : plan_name,
        'period' : period,
        'amount' : amount,
        'gst' : gst,
        'total_amount' : total_amount
    }    
    request.session['order_details_post'] = context
    logger.debug(f"plan_data context : {context}")
    return HttpResponseRedirect("/subscriptions/orders")

def plan_renew(request):
    group_type = request.POST.get('groupcode')
    plan_type = request.POST.get('plancode')
    plan_name = request.POST.get('planname')
    if 'plan_name' in request.POST:
        plan_name = request.POST.get('plan_name')
    period = request.POST.get('period', 'Monthly')
    
    plan = subscriptions.functions.get_plan(plan_type, plan_name, group_type)
    amount = plan.price_per_month if period.lower() == 'monthly' else plan.price_per_year
    gst = .18 * amount
    total_amount = 1.18 * amount
    context = {
        'group_type' : group_type,
        'group_max_members' : users.functions.get_max_members_in_group(group_type),
        'plan_type' : plan_type,
        'plan_name' : plan_name,
        'period' : period,
        'amount' : amount,
        'gst' : gst,
        'total_amount' : total_amount
    }    
    request.session['order_details_post'] = context
    logger.debug(f"plan_renew context : {context}")
    return HttpResponseRedirect("/subscriptions/order-details")

@login_required(login_url='/subscriptions/plans')
def order_details(request):
    POST = request.session['order_details_post']
    group_type = POST.get('group_type')
    plan_type = POST.get('plan_type')
    plan_name = POST.get('plan_name')
    if 'plan_name' in POST:
        plan_name = POST.get('plan_name')
    period = POST.get('period', 'Monthly')
    
    plan = subscriptions.functions.get_plan(plan_type, plan_name, group_type)
    amount = plan.price_per_month if period.lower() == 'monthly' else plan.price_per_year
    gst = .18 * amount
    total_amount = 1.18 * amount
    context = {
        'group_type' : group_type,
        'group_max_members' : users.functions.get_max_members_in_group(group_type),
        'plan_type' : plan_type,
        'plan_name' : plan_name,
        'period' : period,
        'amount' : amount,
        'gst' : gst,
        'total_amount' : total_amount
    }

    request.session['order_details_post'] = context
    logger.debug(f"order_details context : {context}")
    return render(request, 'subscriptions/order_details.html', context = context)
    

@login_required(login_url='/subscriptions/plans')
def create_order(request):
    POST = request.session.get('order_details_post')
    group_mails = request.session.get('data', {}).get('group-mails', request.user.email).split(",")
    amount = POST.get('total_amount', 1)
    period = POST.get('period', 'monthly')
    plan_name = POST.get('plan_name')
    group_type = POST.get('group_type')
    plan_type = POST.get('plan_type')
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'
    notes = {'plan_name': plan_name, 'plan_type' : plan_type, 'group_type' : group_type} 
    DATA = {
                "amount" : int(amount * 100), # Stores, Operates in paise
                "currency" : order_currency,
                "receipt" : order_receipt,
                "notes" : notes,
                "payment_capture" : 1, 
            }
    POST["group_emails"] = group_mails
    try : 
        plan = subscriptions.functions.get_plan_id(plan_name, plan_type, group_type)
        invoice = subscriptions.razorpay.create_razorpay_invoice(request.user, plan, period)
        order = client.order.fetch(invoice["order_id"])
        order["receipt"] = order_receipt
        POST["invoice_id"] = invoice["id"]
        POST["razorpay_order_id"] = order["id"]
        request.session["order_details_post"] = POST
        user_group_id = users.functions.get_user_group(user = request.user, group_type = group_type, create=True)
        subscriptions.functions.register_order(user_group_id = user_group_id, razorpay_order = order)
        context = {
            "order_id" : order["id"],
            "amount" : int(amount * 100), # Stores, Operates in paise
            "currency" : order_currency,
            "plan_details" : "|".join([plan_type, '-'.join(plan_name.split()), group_type]),
            "name" : " ".join([request.user.first_name, request.user.last_name]),
            'email' : request.user.email,
            'contact' : request.user.contact_no,
            'razorpay_key' : RAZORPAY_KEY,
            'group_emails' : group_mails,
            'notes' : notes
        }
    except Exception as e:
        logger.error(f"Error Occured : {e}")
        return JsonResponse({'Exception' : str(e)})
    # return render(request, 'subscriptions/payment.html', context = context)
    return JsonResponse(context)

@login_required(login_url='/subscriptions/plans')
def create_order2(request):
    POST = request.session.get('order_details_post')
    group_mails = request.session.get('data', {}).get('group-mails', request.user.email).split(",")
    amount = POST.get('total_amount', 1)
    plan_name = POST.get('plan_name')
    group_type = POST.get('group_type')
    plan_type = POST.get('plan_type')
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'
    notes = {'plan_name': plan_name, 'plan_type' : plan_type, 'group_type' : group_type}   # OPTIONALclient.order.create(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0')
    DATA = {
                "amount" : int(amount * 100), # Stores, Operates in paise
                "currency" : order_currency,
                "receipt" : order_receipt,
                "notes" : notes,
                "payment_capture" : 0, 
            }
    POST["group_emails"] = group_mails
    request.session["order_details_post"] = POST
    try :
        order = client.order.create(data = DATA)
        user_group_id = users.functions.get_user_group(user = request.user, group_type = group_type, create=True)
        subscriptions.functions.register_order(user_group_id = user_group_id, razorpay_order = order)
        context = {
            "order_id" : order["id"],
            "amount" : amount,
            "currency" : order_currency,
            "plan_details" : "|".join([plan_type, '-'.join(plan_name.split()), group_type]),
            "name" : " ".join([request.user.first_name, request.user.last_name]),
            'email' : request.user.email,
            'contact' : request.user.contact_no,
            'razorpay_key' : RAZORPAY_KEY,
            'group_emails' : group_mails
        }
    except Exception as e:
        logger.error(f"Error Occured : {e}")
        return JsonResponse({'Exception' : str(e)})
    return render(request, 'subscriptions/payment.html', context = context)

def payment_success(request):
    POST = request.session.get('order_details_post') 
    logger.info(f"{request.user.email} : verifying the payment, payment status")
    if request.POST.get("razorpay_invoice_status").lower() not in ["paid", "partially_paid"]:
        #payment not verified sucessfully
        return HttpResponseRedirect(redirect_to="/subscriptions/plans")
    request.session['order_details_post'] = POST
    request.session['order_details_post'].update(
                                            {
                                                'order_id' : POST.get('razorpay_order_id'), 
                                                'payment_id' : request.POST.get('razorpay_payment_id'), 
                                                'signature' : request.POST.get('razorpay_signature')
                                            }
                                        )
    logger.info(f"{request.user.email} : Payment verified successfully, no will be redirected to '/subscriptions/subscribe'")
    return HttpResponseRedirect('/subscriptions/subscribe')

@login_required(login_url='/accounts/login/')
def secure_order_details(request):
    POST = request.session.get('order_details_post')
    group_type, plan_type, plan_name = POST['group_type'], POST['plan_type'], POST['plan_name']
    if not subscriptions.functions.can_subscribe(request.user, group_type, plan_type, plan_name):
        POST["alert"] = True
        request.session['order_details_post'] = POST
        logger.debug(f"secure_order_details context : {POST}")
        return HttpResponseRedirect(redirect_to='/subscriptions/plans')
    if subscriptions.functions.is_trial_applicable(group_type = group_type, plan_type = plan_type, plan_name = plan_type):
        request.session['order_details_post'] = POST
        if not subscriptions.functions.already_had_trial(request.user, group_type, plan_type, plan_name):
            logger.debug(f"secure_order_details context : {POST}")
            return HttpResponseRedirect(redirect_to = "/subscriptions/subscribe")
    request.session['order_details_post'] = POST
    logger.debug(f"secure_order_details context : {POST}")
    return HttpResponseRedirect(redirect_to = '/subscriptions/order-details')

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
    signature = POST.get('signature')
    invoice_id = POST.get('invoice_id')
    payment = subscriptions.functions.register_payment(order_id, payment_id, signature, invoice_id)
    recepients = []
    logger.info(f"{request.user.email} : group mails added for subscriptions are --> {POST.get('group_emails')}")
    if 'group_emails' in POST:    
        email_list = [v.strip() for v in POST['group_emails']]
        recepients.extend(email_list)
    
    subscription_id = subscribe_common(request = request, user = request.user, group_type = group_type, plan_type= plan_type ,   \
                    plan_name= plan_name, period= period, payment_id = payment, recepients=recepients)
    
    return HttpResponseRedirect(redirect_to='/worker/mercury')

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
    group = users.functions.get_group_of_user_from_plan(request.user, POST['plan_name'])
    if subscribed:
        subject = 'Algonauts Plan Subscription Link'
        message = 'This is the link for subscription for group : ' + request.build_absolute_uri(users.functions.generate_group_add_link(group))
        subscriptions.functions.send_email(subscribed.user_group_id, recepient, subject, message)
    return HttpResponseRedirect(redirect_to='/user/profile/info')


def subscribe_common(user, group_type, plan_type, plan_name, period, payment_id, recepients = [], request = None): 
    recepient = [user.email]
    recepients.extend(recepient)
    subscribed = subscriptions.functions.create_subscription(
                    user = user,
                    group_type = group_type,
                    plan_type = plan_type,
                    plan_name = plan_name,
                    period = period,
                    payment_id = payment_id,
                )
    logger.info(f"{request.user.email} : Subscription added for user {user} for plan : {plan_name}, group : {group_type}, plan_type : {plan_type}")
    if subscribed:
        group_add_link = request.build_absolute_uri(users.functions.generate_group_add_link(subscribed.user_group_id))
        subject = "Regarding Algonauts Subscription"
        message = "You have successfully subscribed to algonauts plan : " + str(plan_name) + "\n" + group_add_link
        subscriptions.functions.send_email(user, recepients, subject, message)
    return subscribed

def terminate_subscription(request):
    password = request.POST.get('password', None)
    if password and users.functions.check_password(request.user, password):
        group_type = request.POST.get('groupcode')
        plan_type = request.POST.get('plancode')
        plan_name = request.POST.get('planname')
        if 'plan_name' in request.POST:
            plan_name = request.POST.get('plan_name')
        period = request.POST.get('period', 'monthly')

        if group_type == 'individual': # if plan subscribed by individual group
            plan = subscriptions.functions.get_plan(plan_type, plan_name, group_type)
            subscription_type = subscriptions.functions.get_subscription_type_object(period)
            subscriptions.functions.end_subscription(request.user, plan, subscription_type)

        else : # if plan subscribed by non individual group
            group = users.functions.get_user_group(request.user, group_type)
            users.functions.remove_user_from_group(request.user.email, group_type, group.admin.email)
        return JsonResponse({"success" : True})        
    return JsonResponse({"success" : False})

def historical_purchases(request):
    all_active_subscriptions = subscriptions.functions.get_all_subscriptions_of_user(request.user)

    subs_dict = all_active_subscriptions.values(
                                'plan_id', 
                                'plan_id__user_group_type_id__max_members' , 
                                'plan_id__user_group_type_id__type_name', 
                                'plan_id__plan_name',
                                'plan_id__plan_type_id__type_name', 
                                'user_group_id', 
                                'plan_id__user_group_type_id', 
                                'subscription_type_id__type_name', 
                                'payment_id__invoice_id',
                                'subscription_start',
                                'subscription_end'
                                )
    data = [] # list of dictionaries
    for subscription in subs_dict:    
        data.append({
            "plan-name"     : subscription["plan_id__plan_name"].replace("#", "-"), 
            "plan-type"     : subscription["plan_id__plan_type_id__type_name"], 
            "group-members" : subscription["plan_id__user_group_type_id__max_members"],
            "start-date"    : subscription["subscription_start"].date(),
            "end-date"      : subscription["subscription_end"].date(),        
            "invoice-id"    : subscription['payment_id__invoice_id']
        })

    return JsonResponse({"data" : data})

def download_invoice2(request):
    invoice_id = request.POST.get("invoice_id")
    if invoice_id:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="'+ request.user.first_name + "-"  + invoice_id + '.pdf"'
        fill = requests.get(f"https://invoices.razorpay.com/v1/invoices/{invoice_id}/pdf?download=1&key_id={RAZORPAY_KEY}").content
        response.write(fill)
        return response
    return JsonResponse({"url" : None})

class download_invoice(PDFTemplateView):
    """
    PDFTemplateView with the addition of unicode content in his context.
    Used in unicode content view testing.
    """
    template_name = "subscriptions/invoice_template.html"

    def get(self, request, *args, **kwargs):
            context = self.get_context_data(**kwargs)
            self.filename = '-'.join([context["cust_name"].lower(), 'invoice', 'Mercury', str(context['time_of_supply'])] ) + ".pdf"
            response = super(download_invoice, self).get(request,
                                                    *args, **kwargs)
            return response

    def get_context_data(self, **kwargs): 
        Base = super(download_invoice, self)
        context = Base.get_context_data(**kwargs)
        invoice_id = context["invoice_id"]
        context.update(subscriptions.razorpay.create_invoice_context(invoice_id))
        return context

