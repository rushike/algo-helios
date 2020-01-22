from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('plans', views.plans, name= 'plans_page'),
    path('plan_overview/', views.plan_overview, name='plan_overview_page')

]
