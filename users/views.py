from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView 
from django.contrib.auth.decorators import login_required

import users.functions 

@login_required(login_url = '/accounts/login/')
def profile_page(request):
    iplans, gplans = users.functions.get_user_subs_plans(request.user.id)
    context = {
                'iplans':iplans, 
                'gplans' : gplans,
            }
    
    return render(request, 'users/profile.html', context= context)
    # gid = UserGroupMapping.objects.filter(user_profile_id = request.user)[1].user_group_id
    # get_all_users_in_group(gid)
    # raise EnvironmentError

@login_required(login_url = '/accounts/login/')
def add_referral_credits(request, referral_code):
    logged_user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user
    email = logged_user.email
    users.functions.add_referral_credits(logged_user, referral_code = 	referral_code)
    return render(request, 'users/profile.html')

def create_custom_user_group(request):
    return HttpResponse("Rello")
    
def join_to_group(request, group_id, hash_): #slug in format  str(group_id)<==>md5_hash(admin_email)
    can_add = users.functions.validate_group_add_url_slug(group_id, hash_)
    # raise EnvironmentError
    us = request.user
    logged_user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user
    raise EnvironmentError
    if can_add:
        users.functions.join_to_group(request.user, group_id)
        return HttpResponse("Successfully added to group")
    return HttpResponse("Link invalidate")
