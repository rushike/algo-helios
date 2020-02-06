from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save

import datetime

from users.models import UserGroup, AlgonautsUser, UserGroupType
from subscriptions.models import Plan

# Create your models here.

class ProductCategory(models.Model):
    product_category_name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.product_category_name)

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_category_id = models.ForeignKey(ProductCategory,on_delete=models.CASCADE, related_name="p_product_category_id")
    product_details = models.CharField(max_length=200)
    access_link = models.URLField(max_length=300)
    
    def __str__(self):
        return '#'.join([str(self.product_name), str(self.product_category_id)])
    def __repr__(self):
        return self.__str__()

class PlanProductMap(models.Model):
    plan_id = models.ForeignKey(Plan, on_delete = models.CASCADE, related_name="ppm_plan_id")
    product_id = models.ForeignKey(Product, on_delete = models.CASCADE, related_name="ppm_product_id")
    class Meta:
        unique_together = ('plan_id', 'product_id')
    def __str__(self):
        return "#".join([str(self.product_id), str(self.plan_id)])


class UserProductFilter(models.Model):
    user_id = models.ForeignKey(AlgonautsUser, on_delete= models.CASCADE, related_name="upf_user_id")
    product_id = models.ForeignKey(Product, on_delete = models.CASCADE, related_name="upf_product_id")
    filter_attributes = models.CharField(max_length=200)
    
    def __str__(self):
        return "#".join([str(self.user_id), self.product_id])


def create_individual_plan(sender, instance, **kwargs):
    iGroupType = UserGroupType.objects.get(type_name = 'individual')
    #atomatically creating individual plan for particlar product register
    iplan, _ = Plan.objects.get_or_create(plan_name = '_'.join(['i', str(instance.product_name)]), user_group_type_id = iGroupType, price_per_month = 0, \
             price_per_year = 0, entry_time = datetime.datetime.now(), expiry_time = datetime.datetime.now() , is_active = False)
    pp_map, _ = PlanProductMap.objects.get_or_create(plan_id = iplan, product_id= instance)
    

# post_save.connect(create_individual_plan, Product, dispatch_uid="products.models.Product")

# post_save.connect(create_premium_plan, Plan, dispatch_uid='subscriptions.models.Plan')