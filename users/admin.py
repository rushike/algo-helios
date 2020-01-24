from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import AlgonautsUser, UserGroup, UserGroupMapping, UserGroupType, UserManager, ReferralOffer, Referral

# from myproject.admin_site import custom_admin_site

admin.site.site_header = "Algonauts Administration"

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name' ,'contact_no', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active', 
            'is_staff', 
            'is_superuser',
            'groups', 
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('first_name', 'last_name', 'email', 'contact_no', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('first_name', 'last_name', 'email', 'contact_no')
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(AlgonautsUser, UserAdmin) 

admin.site.register(UserGroup)

admin.site.register(UserGroupMapping)

admin.site.register(UserGroupType)

admin.site.register(Referral)

admin.site.register(ReferralOffer)

