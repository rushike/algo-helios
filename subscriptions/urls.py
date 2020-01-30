from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('plans', views.plans, name='plans_page'),
    path('plan_overview/subscribe',views.plan_subscribe, name=''),
    path('plan_overview/<slug:slug>', views.plan_overview, name='plan_overview_page'),
    # path('plan_subscribe/',views.subscribe, name='plan_subscribe')
]
