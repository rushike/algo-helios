from django.contrib import admin
from .models import Subscription, SubscriptionType,Plan, Offer, OfferPrerequisites, PlanOfferMap, PlanType, Order, Payment


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
            'fields': ('user_group_id', 'plan_id', 'subscription_type_id', 'subscription_start', 'subscription_end', 'is_trial', 'subscription_active' ,'payment_id')
        }),
    )
    
    list_display = ('user_group_id', 'plan_id', 'subscription_type_id', 'subscription_start', 'subscription_end' ,'is_trial', 'subscription_active', 'payment_id')
    list_filter = ('plan_id', 'subscription_type_id', 'subscription_start', 'subscription_end' ,'is_trial', 'subscription_active', 'payment_id')
    search_fields = ('plan_id','user_group_id')
    ordering = ('user_group_id', 'plan_id', 'subscription_type_id', 'subscription_start', 'subscription_end' ,'is_trial', 'subscription_active', 'payment_id')


class PlanAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, 
        {
            'fields': ('plan_name', 'user_group_type_id', 'plan_type_id', 'price_per_month', 'price_per_year' ,'entry_time', 'expiry_time', 'trial_applicable', 'is_active', 'razorpay_plan_per_month_id', 'razorpay_plan_per_year_id')
        }),
    )
    
    list_display = ('plan_name', 'user_group_type_id', 'plan_type_id', 'price_per_month', 'price_per_year' ,'entry_time', 'expiry_time','trial_applicable', 'is_active', 'razorpay_plan_per_month_id', 'razorpay_plan_per_year_id')
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


class OrderAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, 
        {
            'fields': ('razorpay_order_id', 'user_group_id', 'order_amount', 'razorpay_payment_id', 'notes')
        }),
    )
    
    list_display = ('razorpay_order_id', 'user_group_id', 'order_amount', 'razorpay_payment_id')
    list_filter = ('user_group_id', 'razorpay_payment_id', 'order_amount')
    search_fields = ('user_group_id',)
    ordering = ('razorpay_order_id', 'user_group_id', 'order_amount', 'razorpay_payment_id')

class PaymentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, 
        {
            'fields': ('user_group_id', 'order_id', 'payment_ref', 'payment_time', 'amount', 'invoice_id')
        }),
    )

    list_display = ('user_group_id', 'order_id', 'payment_ref', 'payment_time', 'amount', 'invoice_id')
    search_fields = ('user_group_id',)

admin.site.register(Subscription,SubscriptionAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Offer)
admin.site.register(Order, OrderAdmin)
admin.site.register(PlanOfferMap)
admin.site.register(OfferPrerequisites)
admin.site.register(PlanType, PlanTypeAdmin)
admin.site.register(SubscriptionType, SubscriptionTypeAdmin)
admin.site.register(Payment, PaymentAdmin)


