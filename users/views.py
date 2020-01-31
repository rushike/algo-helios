from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView 
from django.contrib.auth.decorators import login_required

from users.functions import *

@login_required(login_url = '/accounts/login/')
def profile_page(request):
    # iplans, gplans = get_user_subs_plans(request.user.id)
    # context = {
    #             'iplans':iplans, 
    #             'gplans' : gplans,
    #         }
    # return render(request, 'users/profile.html', context= context)
    gid = UserGroupMapping.objects.filter(user_profile_id = request.user)[1].user_group_id
    get_all_users_in_group(gid)
    raise EnvironmentError

def create_custom_user_group(request):
    return HttpResponse("Rello")
    
