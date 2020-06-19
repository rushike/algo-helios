from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/info/', views.profile_page, name= "u_profile_page"),
    path('refer/code=<slug:referral_code>', views.add_referral_credits, name= 'u_referral'), # code=<slug : referral_code>
    path('refer/user=<slug:referral_code>', views.join_via_referral_link, name='u_user_referral_sign_up'), 
    path('add-to-group/<int:group_id>/<slug:hash_>', views.join_to_group, name= 'u_join_to_group'), # url with group_id and admin hash
    path('remove-user-from-group/', views.remove_user_from_group, name="remove_user_from_group"),
    path('send-user-add-link/', views.send_user_add_link, name="send_user_add_link"),
    path('get-all-users-in-group/', views.get_all_users_in_group, name="get_all_users_in_group"),
    path('get-user-group-add-link/', views.get_user_group_add_link, name="get_user_group_add_link"),
    path('feedback/', views.get_feedback, name= "feedback"),
    path('register-feedback', views.register_feedback, name= "register_feedback"),
    path('contact-no-edit', views.contact_no_edit, name= "contact_no_edit"),
    path('address-edit', views.address_edit, name= "address_edit"),
    path('get-address', views.get_address, name= "get_address"),
    path('indian-states', views.get_indian_states, name= "indian_states"),
    path('toggle-notification/', views.toggle_notification, name= "toggle_notification"),
]
