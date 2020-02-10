from django.contrib import admin
from django.urls import path, include

from subscriptions import views

urlpatterns = [
    path('plans', views.plans, name='plans_page'),
    path('individual-one', views.individual_one, name ='individual_one'),
    path('individual-premium', views.individual_premium, name ='individual_premium'),
    path('group-one', views.group_one, name ='group_one'),
    path('group-premium', views.group_premium, name ='group_premium'),
    path('subscribe', views.subscribe, name ='subscribe'),
    path('plan_overview/subscribe',views.plan_subscribe, name=''),
    path('plan_overview/<slug:slug>', views.plan_overview, name='plan_overview_page'),
    # path('plan_subscribe/',views.subscribe, name='plan_subscribe')
]
