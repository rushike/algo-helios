from django.contrib import admin
from django.urls import path, include
from subscriptions import views

urlpatterns = [
    path('plans', views.plans2, name='plans_page'),
    path('subscribe', views.subscribe, name ='subscribe'),
    path('can_subscribe', views.can_subscribe, name ='subscribe'),
    path('neft-details', views.neft_details, name ='neft_details'),
    path('create-order', views.create_order, name ='create_order'),
    path('send-neft-details', views.send_neft_details, name = 'send_neft_details'),
    path('orders', views.secure_order_details, name= 'orders'),
    path('payment/success', views.payment_success, name= 'payment_success'),
    path('plan-data', views.plan_data, name="order-details"),
    path('plan-renew', views.plan_renew, name="order-details"),
    path('order-details', views.order_details, name="order-details"),
    path('plan-overview/subscribe',views.plan_subscribe, name=''),
    path('plan-overview/<slug:slug>', views.plan_overview, name='plan_overview_page'),
    path('terminate-subscription', views.terminate_subscription, name='terminate_subscription'),
    path('historical-purchases', views.historical_purchases, name='historical_purchases'),
    path('download-invoice2', views.download_invoice2, name='download_invoice2'),
    path('download-invoice/<slug:invoice_id>', views.download_invoice.as_view()),
    path('plans2', views.plans2, name='plans_page2'),
    path('mercury-product-data/', views.mercury_product_data, name='mercury_product_data'),
    path('jupiter/', views.jupiter, name='jupiter'),
]
