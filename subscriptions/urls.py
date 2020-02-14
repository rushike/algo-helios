from django.contrib import admin
from django.urls import path, include
from subscriptions import views

urlpatterns = [
    path('plans', views.plans, name='plans_page'),
    path('plans2', views.plans2, name='plans2_page'),
    path('subscribe', views.subscribe, name ='subscribe'),
    path('order-details', views.order_details, name= 'order_details'),
    path('plan_overview/subscribe',views.plan_subscribe, name=''),
    path('plan_overview/<slug:slug>', views.plan_overview, name='plan_overview_page'),
]
