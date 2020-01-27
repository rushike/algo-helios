from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/<slug:uid>', views.ProfilePage.as_view(), name="u_profile_page"),
]
