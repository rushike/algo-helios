from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView 
from django.contrib.auth.decorators import login_required

from users.functions import *

@login_required(login_url = '/accounts/login/')
def profile_page(request, uid):
    x = get_user_subs_plans(request.user)
    # y = get_all_users_in_group(request.user)
    raise AttributeError
