from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "worker"

urlpatterns = [
    path('status/', views.get_health_status, name='status'),
    path('mercury2/', views.mercury2, name='mercury2'),
    path('mercury/', views.mercury, name='mercury'),
    path('get-filters/', views.get_filters, name='get_filters'),
    path('apply-filters/', views.apply_filters3, name='apply_filters3'),
    path('apply-filters2/', views.apply_filters, name='apply_filters'),
    path('user_channel_groups/', views.get_user_channel_groups, name = "user_channel_groups"),
    path('get-instrument-from-portfolio/', views.get_instruments_from_portfolio, name = "fetch_instruments"),
    path('get-instruments-for-portfolios/', views.get_instruments_for_portfolios, name = "fetch_all_instruments"),
    path('clear-filter/', views.clear_filter, name = "clear_filter"),
    path('clear-filter2/', views.clear_filter2, name = "clear_filter2"),
    path('calls-from-db/', views.get_calls_from_db, name = "calls_from_db"),
    path('calls-from-db2/', views.get_calls_from_db2, name = "calls_from_db2")
]
