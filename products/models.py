from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save

import datetime, pytz

from users.models import UserGroup, AlgonautsUser, UserGroupType
from subscriptions.models import Plan, PlanType

# Create your models here.

class ProductFamily(models.Model):
    parent_product_name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)

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
    gGroupType = UserGroupType.objects.get(type_name = 'enterprise')
    #atomatically creating individual plan for particlar product register
    iplan, _ = Plan.objects.get_or_create(plan_name = '_'.join(['i', str(instance.product_name)]), user_group_type_id = iGroupType, price_per_month = 0, \
             price_per_year = 0, entry_time = datetime.datetime.now(), expiry_time = datetime.datetime.now())
    pp_map, _ = PlanProductMap.objects.get_or_create(plan_id = iplan, product_id= instance)

    gplan, _ = Plan.objects.get_or_create(plan_name = '_'.join(['g', str(instance.product_name)]), user_group_type_id = gGroupType, price_per_month = 0, \
             price_per_year = 0, entry_time = datetime.datetime.now(), expiry_time = datetime.datetime.now())
    pp_map, _ = PlanProductMap.objects.get_or_create(plan_id = gplan, product_id= instance)


def create_standard_plans(sender, instance, **kwargs):
    group_types =  UserGroupType.objects.all()  # returns all standard group
    plan_types =  PlanType.objects.all()  # returns all plan type, e.g. Basic, Premium
    BASIC = plan_types.get(type_name = "Basic")
    now = datetime.datetime.now(pytz.timezone('UTC'))
    end_date = now + datetime.timedelta(730)
    if not BASIC : raise AttributeError("There is not any 'Basic' plan type in database")
    
    product_name = str(instance.product_name)

    # Create a new BASIC plan for each product is created for all group type ids
    for group_t in group_types:
        plan_exists = Plan.objects.filter(plan_name = product_name, plan_type_id = BASIC, user_group_type_id = group_t).exists()
        if not plan_exists:
            plan, created= Plan.objects.get_or_create(
                            plan_name = product_name, 
                            user_group_type_id = group_t, 
                            plan_type_id = BASIC, 
                            price_per_month = 0,
                            price_per_year = 0,
                            entry_time = now,
                            expiry_time = end_date,
                            is_active = False,
                            trial_applicable = True 
                            )
        plan = Plan.objects.get(plan_name = product_name, plan_type_id = BASIC, user_group_type_id = group_t)
        PlanProductMap.objects.create(
                            plan_id = plan,
                            product_id = instance,
                            )

    # Create a single PREMIUM plan, for all group ids
    PREMIUM = plan_types.get(type_name = "Premium")
    for group_t in group_types:
        plan_exists = Plan.objects.filter(plan_type_id = PREMIUM, user_group_type_id = group_t).exists()
        if not plan_exists:
            plan, created = Plan.objects.get_or_create(
                            plan_name = str(PREMIUM.type_name), 
                            user_group_type_id = group_t, 
                            plan_type_id = PREMIUM, 
                            price_per_month = 0,
                            price_per_year = 0,
                            entry_time = now,
                            expiry_time = end_date,
                            is_active = False,
                            trial_applicable = True 
                            )
            # if created:
        plan = Plan.objects.get(plan_name = str(PREMIUM.type_name), plan_type_id = PREMIUM, user_group_type_id = group_t)
        PlanProductMap.objects.create(
                            plan_id = plan,
                            product_id = instance,
                            )
        # Create Product - Plan map for PREMIUM PLAN
        
    pass


    

# post_save.connect(create_individual_plan, Product, dispatch_uid="products.models.Product")
post_save.connect(create_standard_plans, Product, dispatch_uid="products.models.Product")

# post_save.connect(create_premium_plan, Plan, dispatch_uid='subscriptions.models.Plan')