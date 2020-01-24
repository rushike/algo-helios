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

class GroupMappingAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user_group_id', 'user_profile_id', 'time_added', 'time_removed', 'group_admin')}),
    )
    # ('Permissions', {'fields': (
    #         'group_admin',
    #     )}),
    list_display = ('user_group_id', 'user_profile_id', 'time_added', 'time_removed', 'group_admin')
    list_filter = ('group_admin',)
    search_fields = ('user_profile_id', )
    ordering = ('user_group_id', 'user_profile_id', 'time_added', 'time_removed', 'group_admin')
    # filter_horizontal = ('group_admin', )

class GroupAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user_group_type_id', 'registration_time')}),
    )
    list_display = ('user_group_type_id', 'registration_time')
    list_filter = ('user_group_type_id',)
    search_fields = ('user_group_type_id', )
    ordering = ('user_group_type_id', 'registration_time')


class GroupTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('type_name', 'max_members', 'min_members', 'standard_group')}),
    )
    list_display = ('type_name', 'max_members', 'min_members', 'standard_group',)
    list_filter = ('type_name', 'max_members', 'min_members', 'standard_group',)
    search_fields = ('type_name', )
    ordering = ('type_name', 'max_members', 'min_members', 'standard_group',)


admin.site.register(AlgonautsUser, UserAdmin) 

admin.site.register(UserGroup, GroupAdmin)

admin.site.register(UserGroupMapping, GroupMappingAdmin)

admin.site.register(UserGroupType, GroupTypeAdmin)

admin.site.register(Referral)

admin.site.register(ReferralOffer)

