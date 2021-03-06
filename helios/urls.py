from django.contrib import admin
from django.urls import path, include
from catalog import views
import datetime

urlpatterns = [
    path('', include('catalog.urls')),
    path('admin/login/', views.HomeRedirect, name="admin_login_disable"),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls'), name='blog_urls'),
    path('user/', include('users.urls')),
    path('path-not-found-404', views.ERR404),
    path('subscriptions/', include('subscriptions.urls')),
    path('worker/', include('worker.urls')),
    path('webpush/', include('webpush.urls')),
    path('template/', views.TemplateView.as_view(template_name='subscriptions/invoice_template.html')),
]
