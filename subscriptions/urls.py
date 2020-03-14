from django.contrib import admin
from django.urls import path, include
from subscriptions import views

urlpatterns = [
    path('plans', views.plans, name='plans_page'),
    path('subscribe', views.subscribe, name ='subscribe'),
    path('can_subscribe', views.can_subscribe, name ='subscribe'),
    path('neft-details', views.neft_details, name ='neft_details'),
    path('create-order', views.create_order, name ='create_order'),
    path('send-neft-details', views.send_neft_details, name = 'send_neft_details'),
    path('orders', views.secure_order_details, name= 'orders'),
    path('payment/success', views.payment_success, name= 'payment_success'),
    path('order-details', views.order_details, name="order-details"),
    path('order-details2', views.order_details2, name="order-details"),
    path('plan-overview/subscribe',views.plan_subscribe, name=''),
    path('plan-overview/<slug:slug>', views.plan_overview, name='plan_overview_page'),
]
