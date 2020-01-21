from django.db import models
from .products import models


class Subscription(models.Model):
    subscription_id = models.IntegerField(primary_key=True)
    user_group_id = models.IntegerField #
    plan_id = models.IntegerField #
    subscription_start = models.DateTimeField()
    subscription_end = models.DateTimeField()
    subscription_active = models.BooleanField()
    payment_id = models.IntegerField(default=0)  


