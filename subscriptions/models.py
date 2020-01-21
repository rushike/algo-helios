from django.db import models

from products.models import Plan
from users.models import UserGroup

class Subscription(models.Model):
    # subscription_id = models.IntegerField(primary_key=True)
    user_group_id = models.ForeignKey(UserGroup, on_delete=models.CASCADE)  #
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE) #
    subscription_start = models.DateTimeField()
    subscription_end = models.DateTimeField()
    subscription_active = models.BooleanField()
    payment_id = models.IntegerField(default=0)  




