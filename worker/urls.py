from django.urls import path
from . import views

app_name = "worker"

urlpatterns = [
    path('status/', views.get_health_status, name='status'),
    path('mercury/', views.mercury, name='mercury'),
    path('get-filters/', views.get_filters, name='get_filters'),
    path('apply-filters/', views.apply_filters, name='apply_filters'),
]
