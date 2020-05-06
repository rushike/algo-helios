from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
import logging, json
from allauth.account.signals import user_signed_up, user_logged_in
import users
import users.functions, subscriptions.functions
from django.core import serializers

logger = logging.getLogger('normal')

def remove_hash_from_product(product):
    if '#' in product.product_name: return product.product_name.split('#')[1]
    return product.product_name

@login_required(login_url = '/accounts/login/')
def profile_page(request):
    iplans, gplans = users.functions.get_user_subs_plans(request.user.id) # return objects of type : Subscriptions
    referral_link = request.build_absolute_uri(users.functions.generate_referral_user_add_link(request.user))
    if_referred = users.functions.if_referred(request.user)
    iplans_objs = subscriptions.functions.get_all_plans_from_ids(iplans.values("plan_id"), preserve_length = True)
    gplans_objs = subscriptions.functions.get_all_plans_from_ids(gplans.values("plan_id"), preserve_length = True)
    iplans_type = subscriptions.functions.get_plan_type_of_plans(iplans_objs, preserve_length = True)
    gplans_type = subscriptions.functions.get_plan_type_of_plans(gplans_objs, preserve_length = True)
    iproduct_list = [subscriptions.functions.get_all_products_in_plan(plan_id = plan_name, return_list = True) for plan_name in iplans_objs]
    iproduct_family = [list(subscriptions.functions.get_product_family_of_products(products = [prod])[0] for prod in iprod)[0] for iprod in iproduct_list]

    gproduct_list = [subscriptions.functions.get_all_products_in_plan(plan_id = plan_name, return_list = True) for plan_name in gplans_objs]
    gproduct_family = [list(subscriptions.functions.get_product_family_of_products(products = [prod])[0] for prod in gprod)[0] for gprod in gproduct_list]
    
    iiplans = [[iplans[i], iplans_type[i], iproduct_family[i], remove_hash_from_product(iproduct_list[i][0])] for i in range(len(iplans))]
    ggplans = [[gplans[i], gplans_type[i], gproduct_family[i], remove_hash_from_product(gproduct_list[i][0])] for i in range(len(gplans))]
    context = {
                'iplans':iiplans, 
                'gplans' : ggplans,
                'referral_link' : referral_link,
                'if_referred' : if_referred,
                'is_verified' : users.functions.user_is_verified(request.user)
            }
    return render(request, 'users/profile.html', context= context)


@login_required(login_url = '/accounts/login/')
def add_referral_credits(request, referral_code):
    logged_user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user
    users.functions.add_referral_credits(logged_user, referral_code=referral_code)
    return HttpResponseRedirect('/user/profile/info')

def get_all_users_in_group(request):
    group_type = request.POST.get("groupcode", 'enterprise')
    group_id = users.functions.get_user_group(request.user.email, group_type)
    usersingroups = users.functions.get_all_users_in_group(group_id)
    logger.debug(f"request for all users in group {group_id}, by user {request.user.email}, user members : {usersingroups}")
    usersingroups = [v for v in usersingroups.values("first_name", "last_name", "email")]
    return JsonResponse(usersingroups, safe=False)

@login_required(login_url = '/accounts/login/')    
def join_to_group(request, group_id, hash_): #slug in format  str(group_id)<==>md5_hash(admin_email)
    can_add = users.functions.validate_group_add_url_slug(group_id, hash_) # checks if link is validated and with right credentials
    if can_add:
        obj = users.functions.join_to_group(request.user, group_id)
        if obj: return HttpResponseRedirect(redirect_to='/user/profile/info')
        return HttpResponse("<h1>You might be already present in Group</h1>")
    return HttpResponse("<h1>Link Invalidate</h1>")

def send_user_add_link(request):
    group_type = request.POST.get("groupcode", 'enterprise')
    email = request.POST.get("email")
    logger.debug(f"Got the group-type : {group_type},  email : {email}, admin : {request.user.email}")
    link = users.functions.get_user_add_group_link(request.user.email, group_type)
    if link:
        link = request.build_absolute_uri(link)
        subject = "Regarding Algonauts Subscription"
        message = "You have successfully subscribed to algonauts plan : \n" + link
        subscriptions.functions.send_email(None, email, subject, message)
        logger.debug(f"sending email to user : {email}, subject : {subject}, message : {message}")
        return HttpResponse("ok")
    return HttpResponse("Err")

def get_user_group_add_link(request):
    group_type = request.POST.get("groupcode", 'enterprise')
    email = request.POST.get("email")
    logger.debug(f"Got the group-type : {group_type},  email : {email}, admin : {request.user.email}")
    link = users.functions.get_user_add_group_link(request.user.email, group_type)
    if link:
        link = request.build_absolute_uri(link)
        return JsonResponse({'link' : link, 'groupcode' : group_type}, safe=False)
    return JsonResponse({'link' : None, 'groupcode' : group_type}, safe=False)

@login_required(login_url = '/accounts/login/')
def remove_user_from_group(request):
    email = request.POST.get("email")
    group_type = request.POST.get("groupcode", 'enterprise')
    logger.debug(f"user remove requested for user email : {email},  group_type : {group_type}")
    users.functions.remove_user_from_group(email, group_type, request.user.email)
    return HttpResponse("ok")


@login_required(login_url = '/accounts/signup/')
def join_via_referral_link(request, referral_code):
    if not request.user.is_authenticated:
        return render(request,'account/before-signup.html', context = {'referral_code' : referral_code})
    return HttpResponseRedirect('/user/refer/code=' + str(referral_code))


@login_required(login_url = '/accounts/login/')
def get_feedback(request):
    return render(request,'users/feedback.html')


def register_feedback(request):
    fbdata = dict(request.POST)

    users.functions.add_feedback(request.user, fbdata["subject"][0], fbdata['product-name'][0], fbdata['feedback-message'][0])
    
    return HttpResponseRedirect('/user/profile/info')


@receiver(user_signed_up)
def redirect_after_signup(request, user, **kwargs):
    request.session["REDIRECT_URL"] = "/subscriptions/plans"
    referral_code = request.POST.get("referral-code", "")
    email =  request.POST.get("email", "")
    logged_user = users.functions.get_user_object(email)
    if referral_code != '':
        users.functions.add_referral_credits(logged_user, referral_code=referral_code)
    return HttpResponseRedirect("/products/")

# EDIT section 

def contact_no_edit(request):
    contact_no =  request.POST.get("contact_no", request.user.contact_no)
    users.functions.contact_no_edit(request.user, contact_no)  #function call
    logger.info(f"contact no edited successfully for user : {request.user.email}")
    return JsonResponse({"success":True, "contact_no":contact_no})


