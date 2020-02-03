from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/info', views.profile_page, name= "u_profile_page"),
    path('refer/<slug:referral_code>', views.add_referral_credits, name= 'u_referral'), # <slug : referral_code>
    
    path('add_to_group/<int:group_id>/<slug:hash_>', views.join_to_group, name= 'u_join_to_group'), # url with group_id and admin hash
]
