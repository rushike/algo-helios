from django.db import models
from users.models import UserGroupType, UserGroup
# from products.models import Product, ProductCategory

class Plan(models.Model):
    plan_name = models.CharField(max_length=50)
    user_group_type_id = models.ForeignKey(UserGroupType, on_delete=models.CASCADE)
    price_per_month = models.PositiveIntegerField()
    price_per_year = models.PositiveIntegerField()
    entry_time = models.DateTimeField()
    expiry_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return str(self.plan_name)

class Subscription(models.Model):
    user_group_id = models.ForeignKey(UserGroup, on_delete=models.CASCADE)  #
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE) #
    subscription_start = models.DateTimeField()
    subscription_end = models.DateTimeField()
    subscription_active = models.BooleanField()
    payment_id = models.IntegerField(default=0) 
    def __str__(self):
        return str(self.user_group_id)
