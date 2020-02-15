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
    path('path_not_found_404', views.ERR404),
    path('subscriptions/', include('subscriptions.urls')),
]

# urlpatterns.insert(0, path('admin=' + str(datetime.datetime.now().date()), admin.site.urls))