from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView 
from django.contrib.auth.decorators import login_required

from users.functions import *

@login_required(login_url = '/accounts/login/')
def profile_page(request, uid):
    get_user_subs_product(request.user)
    
    HttpResponse("END")
    