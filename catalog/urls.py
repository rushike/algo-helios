from django.contrib import admin
from django.urls import path, include
from catalog import views

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='index'),
    path('index/', views.IndexPageView.as_view(), name='index'),
    path('aboutus/', views.AboutUsPageView.as_view(), name='aboutus'),
    path('whatwedo/', views.WhatWeDoPageView.as_view(), name='whatwedo'),
    path('products/', views.ProductsPageView.as_view(), name='products'),
]
