from django.shortcuts import render
from django.views.generic import TemplateView 



class ProfilePage(TemplateView):
    template_name = "users/profile.html"