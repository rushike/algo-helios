from django.db import models
from users.models import UserGroupType, UserGroup, UserGroupMapping
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

class PlanManager(models.Manager):
    def create_plan(self,plan_name, user_group_type_id, plan_type_id, price_per_month, price_per_year, entry_time, expiry_time, trial_applicable = None):
        exists = Plan.objects.filter(plan_name = plan_name, user_group_type_id = user_group_type_id, plan_type_id = plan_type_id)
        if exists.exists(): return exists
        if type(user_group_type_id) == int and type(plan_type_id) == int:
            user_group_type_id = UserGroupType.objects.get(id = user_group_type_id)
            plan_type_id = PlanType.objects.get(id = plan_type_id) 
        if not trial_applicable:
            trial_applicable =  user_group_type_id.eligible_for_trial and plan_type_id.trial_applicable
        
        plan_type = self.model(
                                plan_name = plan_name,
                                user_group_type_id = user_group_type_id,
                                plan_type_id = plan_type_id, 
                                price_per_month = price_per_month,
                                price_per_year = price_per_year,
                                entry_time = entry_time,
                                expiry_time = expiry_time,
                                trial_applicable = trial_applicable,
                            )
    
        plan_type.save(using = self._db)
        return plan_type
        
    def get_or_create_plan(self,plan_name, user_group_type_id, plan_type_id, price_per_month, price_per_year, entry_time, expiry_time, trial_applicable = None, is_active = False ):
        exists = Plan.objects.filter(plan_name = plan_name, user_group_type_id = user_group_type_id, plan_type_id = plan_type_id)
        if exists.exists(): return exists
        return self.create_plan(plan_name, user_group_type_id, plan_type_id, price_per_month, price_per_year, entry_time, expiry_time, trial_applicable), True

class Plan(models.Model):
    plan_name = models.CharField(max_length=40)
    user_group_type_id = models.ForeignKey(UserGroupType, on_delete=models.CASCADE)
    plan_type_id = models.ForeignKey(PlanType, on_delete=models.CASCADE)
    price_per_month = models.PositiveIntegerField()
    price_per_year = models.PositiveIntegerField()
    entry_time = models.DateTimeField()
    expiry_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    trial_applicable = models.BooleanField(default= False)
    objects = PlanManager()
    
    class Meta:
        unique_together = ('plan_name', 'user_group_type_id', 'plan_type_id') 
    @staticmethod
    def update_trial_applicable_to_default():
        now = datetime.datetime.now(pytz.timezone('UTC'))
        active_plans = Plan.objects.filter(entry_time__lt = now, expiry_time__gt = now)
        for plan in active_plans:
            plan.trial_applicable = plan.user_group_type_id.eligible_for_trial and plan.plan_type_id.trial_applicable
            plan.save()

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


class Order(models.Model):
    razorpay_order_id = models.CharField(max_length=1024)
    user_group_id = models.ForeignKey(UserGroup, on_delete = models.CASCADE, null = True, default = None)
    order_time = models.DateTimeField(auto_now=True)
    order_amount = models.IntegerField()
    order_currency = models.CharField(max_length=16)
    order_receipt = models.CharField(max_length=1024)
    notes = models.CharField(max_length=1024)
    razorpay_payment_id = models.CharField(max_length=1024, null = True, default = None)
    offer_id = models.CharField(max_length=128, null = True, default = None)

    class Meta:
        unique_together = ("razorpay_order_id",)
    def __str__(self):
        return str(self.razorpay_order_id)


class PaymentManager(models.Manager):
    def create_payment_entry(self):
        pass


class Payment(models.Model):
    payment_ref = models.CharField(max_length=256)
    order_id = models.ForeignKey(Order, on_delete = models.CASCADE, null = True, default = None)
    payment_time = models.DateTimeField(auto_now=True)
    signature = models.CharField(max_length=256, null= True, default = None)
    user_group_id = models.ForeignKey(UserGroup, on_delete = models.CASCADE)
    amount = models.IntegerField()


class SubscriptionType(models.Model):
    type_name = models.CharField(max_length=64)
    duration_in_days = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return '#'.join([str(self.type_name), str(self.duration_in_days)]) 
        

class SubscriptionManager(models.Manager):
    def create_subscription(self, user, group_type, plan_type, plan_name, period, payment_id):
        # user_plan is an array type
        user_group_type_id = UserGroupType.objects.filter(type_name = group_type).first() # group type is string 
        plan_type_id = PlanType.objects.filter(type_name = plan_type).first() # plan type is string
        plan_id = Plan.objects.filter(plan_name=plan_name, user_group_type_id = user_group_type_id, plan_type_id = plan_type_id).first()
        #one user linked with multiple groups
        user_group_id = UserGroup.objects.create_user_group(user_group_type_id, admin=user)

        now = datetime.datetime.now(pytz.timezone('UTC'))

        subscription_type = SubscriptionType.objects.filter(type_name__iexact = period).first()
        
        period = subscription_type.duration_in_days
        subscription_start = datetime.datetime.now(pytz.timezone('UTC'))
        prev_end_date = Subscription.objects.filter(plan_id = plan_id, user_group_id = user_group_id) \
                    .order_by('subscription_end').last() # get the latest entry in the table

        if prev_end_date:
            prev_end_date = prev_end_date.subscription_end
            if subscription_start < prev_end_date:
                subscription_start = prev_end_date 

        if payment_id and (Subscription.objects.filter(user_group_id=user_group_id).exists() or not plan_id.trial_applicable):
            is_trial = False
            subscription_end = subscription_start + datetime.timedelta(days=period) 
        else:
            is_trial = True
            subscription_type = SubscriptionType.objects.filter(type_name__iexact = 'Trial').first()         
            subscription_end = subscription_start + datetime.timedelta(days=1)

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


class Subscription(models.Model):
    user_group_id = models.ForeignKey(UserGroup, on_delete=models.CASCADE) 
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE) 
    offer_id = models.ForeignKey(Offer, on_delete=models.DO_NOTHING, null = True, default = None)
    subscription_type_id = models.ForeignKey(SubscriptionType, on_delete= models.CASCADE)
    subscription_start = models.DateTimeField()
    subscription_end = models.DateTimeField()
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE, null = True, default = None) 
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



