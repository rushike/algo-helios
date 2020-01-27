from django.db import models
from django.utils import timezone

from users.models import UserGroup, AlgonautsUser

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
        return str(self.product_name)

class PlanProductMap(models.Model):
    plan_id = models.ForeignKey(Plan, on_delete = models.CASCADE, related_name="ppm_plan_id")
    product_id = models.ForeignKey(Product, on_delete = models.CASCADE, related_name="ppm_product_id")

    def __str__(self):
        return "#".join([str(self.product_id), str(self.plan_id)])


class UserProductFilter(models.Model):
    user_id = models.ForeignKey(AlgonautsUser, on_delete= models.CASCADE, related_name="upf_user_id")
    product_id = models.ForeignKey(Product, on_delete = models.CASCADE, related_name="upf_product_id")
    filter_attributes = models.CharField(max_length=200)
    pass
