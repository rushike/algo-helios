from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView 
from django.contrib.auth.decorators import login_required
from helios.settings import ABSOLUTE_URL_HOME
import users
import users.functions 

@login_required(login_url = '/accounts/login/')
def profile_page(request):
    iplans, gplans = users.functions.get_user_subs_plans(request.user.id)    
    referral_link = ABSOLUTE_URL_HOME + users.functions.generate_referral_user_add_link(request.user)
    if_referred = users.functions.if_referred(request.user)
    context = {
                'iplans':iplans, 
                'gplans' : gplans,
                'referral_link' : referral_link,
                'if_referred' : if_referred,
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
    users.functions.add_feedback(request.user, fbdata['product-name'][0], fbdata['feedback-message'][0])
    return HttpResponseRedirect('/user/profile/info')