from django.db import models
from users.models import UserGroupType, UserGroup, UserGroupMapping
# from products.models import Product, ProductCategory
import datetime
from django.utils import timezone 
import pytz

class Plan(models.Model):
    plan_name = models.CharField(max_length=50)
    user_group_type_id = models.ForeignKey(UserGroupType, on_delete=models.CASCADE)
    price_per_month = models.PositiveIntegerField()
    price_per_year = models.PositiveIntegerField()
    entry_time = models.DateTimeField()
    expiry_time = models.DateTimeField()
    # is_active = models.BooleanField(default=False)
    @property
    def is_active(self):
        return self.expiry_time > datetime.datetime.now(pytz.timezone('UTC')) or self.entry_time < datetime.datetime.now(pytz.timezone('UTC'))


    def __str__(self):
        return str(self.plan_name)

class OfferPrerequisites(models.Model):
    plan_id = models.ForeignKey( Plan, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.plan_id)
        
class Offer(models.Model):
    offer_name = models.CharField(max_length=20)
    offer_preqreq = models.ForeignKey(OfferPrerequisites, on_delete=models.CASCADE)
    offer_start_date = models.DateTimeField()
    offer_end_date = models.DateTimeField()
    offer_desc = models.CharField(max_length=100) 
    def __str__(self):
        return str(self.offer_name)

class SubscriptionManager(models.Manager):
    def create_subscription(self, plan_name,user, t_delta, payment_id):
        # user_plan is an array type
            user_plan = Plan.objects.filter(plan_name=plan_name)[0]
            #one user linked with multiple groups
            ne = UserGroup.objects.create_user_group(user_plan.user_group_type_id, admin=user)
            ugti = user_plan.user_group_type_id.id
            usermpa = UserGroupMapping.objects.all()
            u_gid = UserGroupMapping.objects.all().values('user_group_id','user_profile_id','user_group_id__user_group_type_id') \
                .filter(user_profile_id=user, user_group_id__user_group_type_id=user_plan.user_group_type_id)

            now = datetime.datetime.now()
            u_g = UserGroup.objects.get(id=u_gid[0]['user_group_id'])
            live_offer_id = PlanOfferMap.objects.all().values('offer_id','plan_id','offer_id__offer_start_date','offer_id__offer_end_date') \
                .filter(offer_id__offer_end_date__gt = now, offer_id__offer_start_date__lt = now)

            live_offer_id = live_offer_id[0]['offer_id']
            live_offer_id = Offer.objects.get(id=live_offer_id)    
 
            subscription_start = datetime.datetime.now(pytz.timezone('UTC'))
            prev_end_date = Subscription.objects.filter(plan_id = user_plan, user_group_id = u_g).order_by('subscription_start').values().last()
            if prev_end_date:
                prev_end_date = prev_end_date['subscription_end']
                if subscription_start < prev_end_date:
                    subscription_start = prev_end_date 

            if Subscription.objects.filter(user_group_id=u_g).exists():
                is_trial = False
                subscription_end = subscription_start + datetime.timedelta(days=t_delta) 
            else:
                is_trial = True         
                subscription_end = subscription_start + datetime.timedelta(days=1)

            valid_trial_group = self.model(user_group_id = u_g,plan_id = user_plan, offer_id =live_offer_id, subscription_start = subscription_start, subscription_end = subscription_end, payment_id = payment_id, is_trial = is_trial)
            valid_trial_group.save(using=self._db)

            return valid_trial_group

    def renew(self):
        pass

    def is_subscribed(self):
        pass
            # raise AttributeError
            

class Subscription(models.Model):
    user_group_id = models.ForeignKey(UserGroup, on_delete=models.CASCADE) 
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE) 
    offer_id = models.ForeignKey(Offer, on_delete=models.DO_NOTHING, null = True)
    subscription_start = models.DateTimeField()
    subscription_end = models.DateTimeField()
    payment_id = models.IntegerField(default=0) 
    is_trial = models.BooleanField(default=False)
    objects = SubscriptionManager()

    def __str__(self):
        return str(self.user_group_id)


class PlanOfferMap(models.Model):
    offer_id = models.ForeignKey( Offer, on_delete=models.CASCADE)
    plan_id = models.ForeignKey( Plan, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.offer_id)

