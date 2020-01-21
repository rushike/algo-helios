from django.db import models
from django.utils import timezone
from users.models import UserGroup
# Create your models here.
   

class AlgoProductCategory(models.Model):
    # id = models.IntegerField(primary_key=True)
    product_category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.product_category_name

class AlgoProduct(models.Model):
    # id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_category_id = models.ForeignKey(AlgoProductCategory,on_delete=models.CASCADE)
    product_details = models.CharField(max_length=200)
    access_link = models.CharField(max_length=100)
    
    def __str__(self):
        return self.product_name



class Plan(models.Model):
    # plan_id = models.IntegerField(primary_key=True)
    plan_name = models.CharField(max_length=500)
    user_group_id = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    price_per_month = models.PositiveIntegerField()
    price_per_year = models.PositiveIntegerField()
    entry_time = models.DateTimeField()
    expiry_time = models.DateTimeField()
    is_active = models.BooleanField()

# class PlanProductsMap(models.Model):
#     plan_product_id = model.IntegerField(primary_key=True)
#     plan_id = models.Model #
#     product_id = models.Model #