from django.contrib import admin
from django.urls import path, include
from catalog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('blog/', include('blog.urls')),
    path('path_not_found_404', views.ERR404),
    path('subscriptions/', include('subscriptions.urls')),
]
