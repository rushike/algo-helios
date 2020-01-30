from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/<slug:uid>', views.profile_page, name="u_profile_page"),
]
