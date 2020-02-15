from django.contrib import admin
from .models import ProductCategory, Product, PlanProductMap, UserProductFilter, ProductFamily


class ProductCategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, 
        {
            'fields': ('product_category_name',)
        }),
    )
    
    list_display = ('product_category_name',)
    list_filter = ('product_category_name',)
    search_fields = ('product_category_name',)
    ordering = ('product_category_name',)


class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, 
        {
            'fields': ('product_name', 'product_family_id', 'product_category_id','product_details',)
        }),
    )
    
    list_display = ('product_name', 'product_family_id', 'product_category_id','product_details')
    list_filter = ('product_name', 'product_family_id', 'product_category_id')
    search_fields = ('product_name', 'product_family_id', 'product_category_id')
    ordering = ('product_name', 'product_family_id', 'product_category_id','product_details')


class PlanProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, 
        {
            'fields': ('plan_id','product_id')
        }),
    )
    
    list_display = ('plan_id','product_id')
    list_filter = ('plan_id','product_id')
    search_fields = ('plan_id','product_id')
    ordering = ('plan_id','product_id')


class UserProductFilterAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, 
        {
            'fields': ('user_id','product_id', 'filter_attributes')
        }),
    )
    
    list_display = ('user_id','product_id', 'filter_attributes')
    list_filter = ('user_id','product_id', 'filter_attributes')
    search_fields = ('product_id',)
    ordering = ('user_id','product_id', 'filter_attributes')


class ProductFamilyAdmin(admin.ModelAdmin):
    fieldsets = ( 
        (None,
        {
            'fields' : ('parent_product_name', 'description')
        }),
    )
    
    list_display = ('parent_product_name', 'description')
    list_filter = ('parent_product_name', 'description')
    search_fields = ('parent_product_name', 'description')
    ordering = ('parent_product_name', 'description')


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductFamily, ProductFamilyAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(PlanProductMap, PlanProductAdmin)
admin.site.register(UserProductFilter, UserProductFilterAdmin)