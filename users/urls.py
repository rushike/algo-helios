from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/info', views.profile_page, name= "u_profile_page"),
    path('refer/code=<slug:referral_code>', views.add_referral_credits, name= 'u_referral'), # code=<slug : referral_code>
    path('refer/user=<slug:referral_code>', views.join_via_referral_link, name='u_user_referral_sign_up'), 
    path('add-to-group/<int:group_id>/<slug:hash_>', views.join_to_group, name= 'u_join_to_group'), # url with group_id and admin hash
    path('feedback', views.get_feedback, name= "feedback"),
    path('register-feedback', views.register_feedback, name= "register_feedback"),
]
