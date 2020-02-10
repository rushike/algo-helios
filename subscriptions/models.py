from django.db import models
from users.models import UserGroupType, UserGroup, UserGroupMapping
# from products.models import Product, ProductCategory
import datetime
from django.utils import timezone 
import pytz

class PlanType(models.Model):
    type_name = models.CharField(max_length=64)
    type_description = models.CharField(max_length=1024)
    products_count = models.IntegerField(default=1)
    trial_applicable = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return str(self.type_name)

class Plan(models.Model):
    plan_name = models.CharField(max_length=50)
    user_group_type_id = models.ForeignKey(UserGroupType, on_delete=models.CASCADE)
    plan_type_id = models.ForeignKey(PlanType, on_delete=models.CASCADE)
    price_per_month = models.PositiveIntegerField()
    price_per_year = models.PositiveIntegerField()
    entry_time = models.DateTimeField()
    expiry_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    trial_applicable = models.BooleanField(default= False)
    objects = models.Manager()
    
    # @property
    # def is_active(self):
    #     return self.expiry_time > datetime.datetime.now(pytz.timezone('UTC')) or self.entry_time < datetime.datetime.now(pytz.timezone('UTC'))

    class Meta:
        unique_together = ('plan_name', 'user_group_type_id', 'plan_type_id') 

    def __str__(self):
        return "#".join([str(self.plan_name), str(self.user_group_type_id), str(self.plan_type_id)])

class OfferPrerequisites(models.Model):
    plan_id = models.ForeignKey( Plan, on_delete=models.CASCADE, null = True, default= None)
    objects = models.Manager()
    def __str__(self):
        return str(self.plan_id)
        
class Offer(models.Model):
    offer_name = models.CharField(max_length=20, null=True, default= None)
    offer_preqreq = models.ForeignKey(OfferPrerequisites, on_delete=models.CASCADE)
    offer_start_date = models.DateTimeField()
    offer_end_date = models.DateTimeField()
    offer_desc = models.CharField(max_length=100) 
    objects = models.Manager()
    def __str__(self):
        return str(self.offer_name)

class SubscriptionType(models.Model):
    type_name = models.CharField(max_length=64)
    duration_in_days = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return '#'.join([str(self.type_name), str(self.duration_in_days)]) 
        

class SubscriptionManager(models.Manager):
    def create_subscription(self, user, group_type, plan_type, plan_name, period, payment_id):
        # user_plan is an array type
        user_group_type_id = UserGroupType.objects.get(type_name = group_type) # group type is string 
        plan_id = Plan.objects.filter(plan_name=plan_name, user_group_type_id = user_group_type_id).first()
        #one user linked with multiple groups
        user_group_id = UserGroup.objects.create_user_group(user_group_type_id, admin=user)
        # ugti = plan_id.user_group_type_id.id
        # usermpa = UserGroupMapping.objects.all()
        # u_gid = UserGroupMapping.objects.all().values('user_group_id','user_profile_id','user_group_id__user_group_type_id') \
        #     .filter(user_profile_id=user, user_group_id__user_group_type_id=plan_id.user_group_type_id)
        # user_group_id = UserGroup.objects.get(id=u_gid[0]['user_group_id'])

        now = datetime.datetime.now()
        
        subscription_type = SubscriptionType.objects.filter(type_name__iexact = period).first()
        period = subscription_type.duration_in_days

        subscription_start = datetime.datetime.now(pytz.timezone('UTC'))
        prev_end_date = Subscription.objects.filter(plan_id = plan_id, user_group_id = user_group_id).order_by('subscription_end').last() # get the latest entry in the table


        
        if prev_end_date:
            prev_end_date = prev_end_date.subscription_end
            if subscription_start < prev_end_date:
                subscription_start = prev_end_date 

        if Subscription.objects.filter(user_group_id=user_group_id).exists():
            is_trial = False
            subscription_end = subscription_start + datetime.timedelta(days=period) 
        else:
            is_trial = True
            subscription_type = SubscriptionType.objects.filter(type_name__iexact = 'Trial').first()         
            subscription_end = subscription_start + datetime.timedelta(days=1)

        # raise EnvironmentError
        subscription = self.model(
                        user_group_id = user_group_id, 
                        plan_id = plan_id, 
                        offer_id = None, 
                        subscription_type_id = subscription_type,
                        subscription_start = subscription_start, 
                        subscription_end = subscription_end, 
                        payment_id = payment_id, 
                        is_trial = is_trial)
        subscription.save(using=self._db)

        return subscription

    def renew(self):
        pass

    def is_subscribed(self):
        pass
            # raise AttributeError
            

class Subscription(models.Model):
    user_group_id = models.ForeignKey(UserGroup, on_delete=models.CASCADE) 
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE) 
    offer_id = models.ForeignKey(Offer, on_delete=models.DO_NOTHING, null = True, default = None)
    subscription_type_id = models.ForeignKey(SubscriptionType, on_delete= models.CASCADE)
    subscription_start = models.DateTimeField()
    subscription_end = models.DateTimeField()
    payment_id = models.IntegerField(default=0) 
    is_trial = models.BooleanField(default=False)
    subscription_active = models.BooleanField(default=False)
    objects = SubscriptionManager()
    
    def __str__(self):
        return str(self.user_group_id)


class PlanOfferMap(models.Model):
    offer_id = models.ForeignKey( Offer, on_delete=models.CASCADE)
    plan_id = models.ForeignKey( Plan, on_delete=models.CASCADE)
    objects = models.Manager()
    def __str__(self):
        return str(self.offer_id)


class Payment(models.Model):
    payment_ref = models.CharField(max_length=256)
    payment_time = models.DateTimeField(auto_now=True)
    subscription_id = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    user_group_id = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    amount = models.IntegerField()