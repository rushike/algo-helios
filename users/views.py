from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView 
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
import users
import users.functions, subscriptions.functions

@login_required(login_url = '/accounts/login/')
def profile_page(request):
    iplans, gplans = users.functions.get_user_subs_plans(request.user.id) # return objects of type : Subscriptions
    referral_link = request.build_absolute_uri(users.functions.generate_referral_user_add_link(request.user))
    if_referred = users.functions.if_referred(request.user)
    iplans_objs = subscriptions.functions.get_all_plans_from_ids(iplans.values("plan_id"))
    gplans_objs = subscriptions.functions.get_all_plans_from_ids(gplans.values("plan_id"))
    iplans_type = subscriptions.functions.get_plan_type_of_plans(iplans_objs)
    gplans_type = subscriptions.functions.get_plan_type_of_plans(gplans_objs)
    iproduct_list = [subscriptions.functions.get_all_products_in_plan(plan_id = plan_name) for plan_name in iplans_objs]
    iproduct_family = [list(subscriptions.functions.get_product_family_of_products(products = [prod])[0] for prod in iprod)[0] for iprod in iproduct_list]

    gproduct_list = [subscriptions.functions.get_all_products_in_plan(plan_id = plan_name) for plan_name in gplans_objs]
    gproduct_family = [list(subscriptions.functions.get_product_family_of_products(products = [prod])[0] for prod in gprod)[0] for gprod in gproduct_list]
    
    iiplans = [[iplans[i], iplans_type[i], iproduct_family[i]] for i in range(len(iplans))]
    ggplans = [[gplans[i], gplans_type[i], gproduct_family[i]] for i in range(len(gplans))]
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
    
@login_required(login_url = '/accounts/login/')    
def join_to_group(request, group_id, hash_): #slug in format  str(group_id)<==>md5_hash(admin_email)
    can_add = users.functions.validate_group_add_url_slug(group_id, hash_) # checks if link is validated and with right credentials
    if can_add:
        obj = users.functions.join_to_group(request.user, group_id)
        if obj: return HttpResponseRedirect(redirect_to='/user/profile/info')
        return HttpResponse("<h1>You might be already present in Group</h1>")
    return HttpResponse("<h1>Link Invalidate</h1>")

@login_required(login_url = '/accounts/signup/')
def join_via_referral_link(request, referral_code):
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
    return HttpResponseRedirect("/products/")
