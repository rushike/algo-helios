from django.db import models

from users.models import UserGroup


class Plan(models.Model):
    plan_name = models.CharField(max_length=500)
    user_group_id = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    price_per_month = models.PositiveIntegerField()
    price_per_year = models.PositiveIntegerField()
    entry_time = models.DateTimeField()
    expiry_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)

class Subscription(models.Model):
    user_group_id = models.ForeignKey(UserGroup, on_delete=models.CASCADE)  #
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE) #
    subscription_start = models.DateTimeField()
    subscription_end = models.DateTimeField()
    subscription_active = models.BooleanField()
    payment_id = models.IntegerField(default=0)  
    