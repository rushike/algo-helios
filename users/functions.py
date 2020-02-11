from users.models import AlgonautsUser, UserGroup, UserGroupType, UserGroupMapping, ReferralOffer, Referral
from subscriptions.models import Plan, Subscription, SubscriptionType
from products.models import Product, ProductCategory, PlanProductMap
import pytz
import datetime
from hashlib import md5

def join_to_group(user:AlgonautsUser, group_id:UserGroup): # method add user(self) to the specific group with group_id 
    user_group_id  =group_id if type(group_id) == UserGroup else UserGroup.objects.get(id = group_id)
    mapper = UserGroupMapping.objects.create_user_group_mapping(user_profile_id= user, user_group_id=user_group_id, delta_period=4, group_admin= False)
    return mapper

def get_all_standard_groups():
    """
        These are the non-individual group type.
    """
    gtypes = UserGroupType.objects.all() #exclude(type_name = 'individual')
    return gtypes.order_by('max_members')

def generate_group_add_link(group_id:UserGroup):
    group_id = group_id._wrapped if hasattr(group_id,'_wrapped') else group_id # if group id is wrapped by other object e.g. SimplyLazyObject
    group = group_id if type(group_id) == UserGroup else UserGroup.objects.get(id = group_id)
    admin = group.admin.email
    
    id_ = group.id
    link = 'user/add_to_group/' + str(id_) + "/" + md5(str(admin).encode()).hexdigest()
    return link

def validate_group_add_url_slug(group_id:int, hash_:str):
    group = UserGroup.objects.get(id = group_id)
    if md5(str(group.admin.email).encode()).hexdigest() == hash_:
        return True
    return False

def get_user_subs_plans(user):
    user = user if type(user) == AlgonautsUser else AlgonautsUser.objects.get(id = user)
    now = datetime.datetime.now(pytz.timezone('UTC'))
    iGroupType = UserGroupType.objects.get(min_members = 1, max_members = 1 ) # get the individual object from moddles
    eGroupType = UserGroupType.objects.exclude(min_members = 1, max_members = 1) # get rest group types available from model
    #one user linked with multiple groups
    # user_all_groups2 = UserGroupMapping.objects.all().values('user_profile_id', 'user_group_id', 'user_group_id__user_group_type_id')
    user_all_groups = UserGroupMapping.objects.filter(user_profile_id = user).values('user_profile_id', 'user_group_id', 'user_group_id__user_group_type_id').values('user_group_id')
    indivdual =	user_all_groups.filter(user_profile_id=user, user_group_id__user_group_type_id = iGroupType).values('user_group_id__user_group_type_id')
    group = user_all_groups.filter(user_profile_id=user, user_group_id__user_group_type_id__in = eGroupType).values('user_group_id__user_group_type_id') # filter out all groups of profile with non individual group type 
    
    plans = Subscription.objects.filter(user_group_id__in = user_all_groups, subscription_end__gt = now, subscription_start__lt = now).values('plan_id', 'plan_id__plan_name' ,'user_group_id', 'plan_id__user_group_type_id', 'subscription_type_id__type_name', 'plan_id__entry_time', 'plan_id__expiry_time', 'plan_id__price_per_month', 'plan_id__price_per_year','subscription_start','subscription_end')
    # subs = plans.filter(subscription_type_id__in = SubscriptionType.objects.all())
    group_plans = plans.filter(plan_id__user_group_type_id__in = group, plan_id__entry_time__lt = now, plan_id__expiry_time__gt = now )		
    indivdual_plans = plans.filter(plan_id__user_group_type_id__in = indivdual, plan_id__entry_time__lt = now, plan_id__expiry_time__gt = now)
    # raise EnvironmentError
    return indivdual_plans, group_plans

def get_user_subs_product(user):
    iplan, gplan = get_user_subs_plans(user)
    iproducts = PlanProductMap.objects.filter(plan_id__in = iplan)
    gproducts = PlanProductMap.objects.filter(plan_id__in = gplan)

    ig_products = list(iproducts)
    ig_products.extend(gproducts)
    return ig_products

def get_all_users_in_group(group_id):
    group = group_id if type(group_id) == UserGroup else UserGroup.objects.get(id = group_id)
    users = UserGroupMapping.objects.filter(user_group_id = group, time_removed__gt = datetime.datetime.now())
    return users
    
def get_all_groups_of_user(user_id):
    user = user_id if type(user_id) == UserGroup else UserGroup.objects.get(id = user_id)
    groups = UserGroupMapping.objects.filter(user_profile_id = user, time_removed__gt = datetime.datetime.now())
    return groups

def add_referral_credits(self_uid, referral_code):
    ref_by = AlgonautsUser.objects.get(referral_code=referral_code)
    ref_to = self_uid if type(self_uid) == AlgonautsUser else AlgonautsUser.objects.get(id = self_uid)
    referral_offer_id = list(ReferralOffer.objects.filter(offer_active = True).order_by('offer_end'))[-1] # take the latest and only active offer
    referral_time =datetime.datetime.now()
    
    if Referral.objects.filter(referred_to = ref_to).exists():
        return None, False

    algo_credits_to = ref_to.algo_credits + referral_offer_id.offer_credits_to
    algo_credits_by = ref_by.algo_credits + referral_offer_id.offer_credits_by
    AlgonautsUser.objects.filter(email = ref_to.email).update(algo_credits = algo_credits_to)
    AlgonautsUser.objects.filter(email = ref_by.email).update(algo_credits = algo_credits_by)

    ref = Referral.objects.create(
                            referral_code = referral_code, 
                            referral_offer_id = referral_offer_id, 
                            referral_time = referral_time, 
                            referred_to = ref_to, 
                            referred_by=ref_by
                        )
    return ref, True

def generate_referral_user_add_link(user:AlgonautsUser):
    link = 'user/refer/user=' + user.referral_code
    return link

def if_referred(user:AlgonautsUser):
    ref = Referral.objects.filter(referred_by = user).exists()
    return ref
