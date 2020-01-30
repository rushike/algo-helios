from django.shortcuts import render
from django.views.generic import TemplateView 
from Users.models import AlgonautsUser


def profile_page(request,uid):
    template_name = "users/profile.html"
    return render(request, template_name, context=user_info)
