from django.db import models
from django.utils import timezone
from users.models import UserGroup
# Create your models here.

class AlgoProductCategory(models.Model):
    product_category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.product_category_name

class AlgoProduct(models.Model):
    product_name = models.CharField(max_length=50)
    product_category_id = models.ForeignKey(AlgoProductCategory,on_delete=models.CASCADE)
    product_details = models.CharField(max_length=200)
    access_link = models.CharField(max_length=100)
    
    def __str__(self):
        return self.product_name
