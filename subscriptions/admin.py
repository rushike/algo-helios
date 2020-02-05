from django.contrib import admin
from .models import Subscription, Plan, Offer, OfferPrerequisites, PlanOfferMap


class SubscriptionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, 
        {
            'fields': ('user_group_id', 'plan_id', 'subscription_start', 'subscription_end' ,'is_trial', 'payment_id')
        }),
    )
    
    list_display = ('user_group_id', 'plan_id', 'subscription_start', 'subscription_end' ,'is_trial', 'payment_id')
    list_filter = ('user_group_id', 'plan_id', 'subscription_start', 'subscription_end' ,'is_trial', 'payment_id')
    search_fields = ('plan_id','user_group_id')
    ordering = ('user_group_id', 'plan_id', 'subscription_start', 'subscription_end' ,'is_trial', 'payment_id')

class PlanAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, 
        {
            'fields': ('plan_name', 'user_group_type_id', 'price_per_month', 'price_per_year' ,'entry_time', 'expiry_time',)
        }),
    )
    
    list_display = ('plan_name', 'user_group_type_id', 'price_per_month', 'price_per_year' ,'entry_time', 'expiry_time',)
    list_filter = ('plan_name', 'user_group_type_id', 'price_per_month', 'price_per_year' ,'entry_time', 'expiry_time',)
    search_fields = ('plan_name','user_group_type_id')
    ordering = ('plan_name', 'user_group_type_id', 'price_per_month', 'price_per_year' ,'entry_time', 'expiry_time',)


admin.site.register(Subscription,SubscriptionAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Offer)
admin.site.register(PlanOfferMap)
admin.site.register(OfferPrerequisites)
