from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import AlgonautsUser, Address, UserGroup, UserGroupMapping, UserGroupType, UserManager, ReferralOffer, Referral, UserFeedback

admin.site.site_header = "Algonauts Administration"

class AddressAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'line1', 'line2', 'city', 'state', 'zipcode')}),
    )
    list_display = ('email', 'line1', 'line2', 'city', 'state', 'zipcode')
    list_filter = ('city', 'state')
    search_fields = ('state', )
    ordering = ('email', 'line1', 'line2', 'city', 'state', 'zipcode')

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name' ,'contact_no', 'last_login', 'algo_credits','referral_code' , 'allow_notification')}),
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

    list_display = ('first_name', 'last_name', 'email', 'contact_no', 'is_staff', 'last_login', 'algo_credits','referral_code', 'allow_notification' )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('first_name', 'last_name', 'email', 'contact_no', 'algo_credits', 'referral_code' )
    filter_horizontal = ('groups', 'user_permissions',)


class GroupMappingAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user_group_id', 'user_profile_id', 'time_removed', 'group_admin')}),
    )
    list_display = ('user_group_id', 'user_profile_id', 'time_removed', 'group_admin')
    list_filter = ('group_admin',)
    search_fields = ('user_profile_id', )
    ordering = ('user_group_id', 'user_profile_id', 'time_removed', 'group_admin')


class GroupAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ( 'user_group_type_id', 'admin')}),
    )

  
    list_display = ('id', 'user_group_type_id', 'registration_time', 'admin')
    list_filter = ('user_group_type_id',)
    search_fields = ('user_group_type_id', )
    ordering = ('user_group_type_id', 'registration_time', 'admin')


class ReferralOfferAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('offer_name', 'offer_credits_to', 'offer_credits_by', 'offer_end', 'offer_active')}),
    )

    list_display = ('offer_name', 'offer_credits_to', 'offer_credits_by', 'offer_end', 'offer_active',)
    list_filter = ('offer_name', 'offer_credits_to', 'offer_credits_by', 'offer_end', 'offer_active',)
    search_fields = ('offer_name', )
    ordering = ('offer_name', 'offer_credits_to', 'offer_credits_by', 'offer_end', 'offer_active')


class ReferralAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('referral_code', 'referred_by', 'referred_to', 'referred_time', 'referral_offer_id',)}),
    )

    list_display = ('referral_code', 'referred_by', 'referred_to', 'referral_time', 'referral_offer_id',)
    list_filter = ('referral_code', 'referred_by', 'referred_to', 'referral_time', 'referral_offer_id',)
    search_fields = ('referral_code', )
    ordering = ('referral_code', 'referred_by', 'referred_to', 'referral_time', 'referral_offer_id',)


class GroupTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('type_name', 'max_members', 'min_members', 'standard_group' ,'eligible_for_trial', )}),
    )

    list_display = ('type_name', 'max_members', 'min_members', 'standard_group','eligible_for_trial',)
    list_filter = ('type_name', 'max_members', 'min_members', 'standard_group','eligible_for_trial',)
    search_fields = ('type_name', )
    ordering = ('type_name', 'max_members', 'min_members', 'standard_group','eligible_for_trial',)


admin.site.register(AlgonautsUser, UserAdmin) 
admin.site.register(Address, AddressAdmin) 
admin.site.register(UserGroup, GroupAdmin)
admin.site.register(UserGroupMapping, GroupMappingAdmin)
admin.site.register(UserGroupType, GroupTypeAdmin)
admin.site.register(Referral, ReferralAdmin)
admin.site.register(ReferralOffer, ReferralOfferAdmin)
admin.site.register(UserFeedback)

