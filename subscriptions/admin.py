from django.contrib import admin
from .models import Subscription, SubscriptionType,Plan, Offer, OfferPrerequisites, PlanOfferMap, PlanType


class SubscriptionTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, 
        {
            'fields': ('type_name', 'duration_in_days')
        }),
    )

    list_display = ('type_name', 'duration_in_days')
    list_filter = ('type_name', 'duration_in_days')
    search_fields = ('type_name',)
    ordering = ('type_name', 'duration_in_days')


class SubscriptionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, 
        {
            'fields': ('user_group_id', 'plan_id', 'subscription_type_id', 'subscription_start', 'subscription_end', 'is_trial', 'payment_id')
        }),
    )
    
    list_display = ('user_group_id', 'plan_id', 'subscription_type_id', 'subscription_start', 'subscription_end' ,'is_trial', 'payment_id')
    list_filter = ('user_group_id', 'plan_id', 'subscription_type_id', 'subscription_start', 'subscription_end' ,'is_trial', 'payment_id')
    search_fields = ('plan_id','user_group_id')
    ordering = ('user_group_id', 'plan_id', 'subscription_type_id', 'subscription_start', 'subscription_end' ,'is_trial', 'payment_id')


class PlanAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, 
        {
            'fields': ('plan_name', 'user_group_type_id', 'plan_type_id', 'price_per_month', 'price_per_year' ,'entry_time', 'expiry_time', 'trial_applicable', 'is_active')
        }),
    )
    
    list_display = ('plan_name', 'user_group_type_id', 'plan_type_id', 'price_per_month', 'price_per_year' ,'entry_time', 'expiry_time','trial_applicable', 'is_active')
    list_filter = ('plan_name', 'user_group_type_id', 'plan_type_id', 'price_per_month', 'price_per_year' ,'entry_time', 'expiry_time','trial_applicable', 'is_active')
    search_fields = ('plan_name','user_group_type_id')
    ordering = ('plan_name', 'user_group_type_id', 'plan_type_id', 'price_per_month', 'price_per_year' ,'entry_time', 'expiry_time','trial_applicable', 'is_active')


class PlanTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, 
        {
            'fields': ('type_name', 'type_description', 'products_count' ,'trial_applicable')
        }),
    )
    
    list_display = ('type_name', 'type_description', 'products_count','trial_applicable')
    list_filter = ('type_name', 'trial_applicable')
    search_fields = ('type_name',)
    ordering = ('type_name', 'type_description', 'products_count','trial_applicable')


admin.site.register(Subscription,SubscriptionAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Offer)
admin.site.register(PlanOfferMap)
admin.site.register(OfferPrerequisites)
admin.site.register(PlanType, PlanTypeAdmin)
admin.site.register(SubscriptionType, SubscriptionTypeAdmin)


