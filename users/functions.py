from users.models import AlgonautsUser, Address, UserGroup, UserGroupType, UserGroupMapping, ReferralOffer, Referral, UserFeedback
from subscriptions.models import Plan, Subscription, SubscriptionType
from products.models import Product, ProductCategory, PlanProductMap
from allauth.account.admin import EmailAddress
from django.contrib.auth import authenticate
from localflavor.in_.in_states import STATE_CHOICES
import pytz, datetime
from hashlib import md5
import subscriptions.functions
from helios.settings import EMAIL_HOST_USER
from channels.db import database_sync_to_async
import logging


logger = logging.getLogger('normal')

STATE_DICT = dict([(v[1], v[0]) for v in STATE_CHOICES])
REV_STATE_DICT = dict([(v[0], v[1]) for v in STATE_CHOICES])

def get_user_object(user):
    if hasattr(user,'_wrapped') :
        if not user.is_authenticated: return None
        if user._wrapped.__class__ == object:
            user._setup()
        user = user._wrapped
    if type(user) == str:
        user = AlgonautsUser.objects.get(email = user)
    else : user = user if type(user) == AlgonautsUser else AlgonautsUser.objects.get(id = user)
    return user



def join_to_group(user:AlgonautsUser, group_id:UserGroup): # method add user(self) to the specific group with group_id 
    user_group_id  =group_id if type(group_id) == UserGroup else UserGroup.objects.get(id = group_id)
    mapper = UserGroupMapping.objects.create_user_group_mapping(
                                                                user_profile_id= user, 
                                                                user_group_id=user_group_id, 
                                                                group_admin= False, 
                                                                )
    return mapper


def user_is_verified(user):
    user = get_user_object(user)
    if user.is_superuser: return True
    user = user.email
    return EmailAddress.objects.get(email = user).verified


def get_all_standard_groups():
    """
        These are the non-individual group type.
    """
    gtypes = UserGroupType.objects.all() 
    return gtypes.order_by('max_members')


def generate_group_add_link(group_id:UserGroup):
    group_id = group_id._wrapped if hasattr(group_id,'_wrapped') else group_id # if group id is wrapped by other object e.g. SimplyLazyObject
    group = group_id if type(group_id) == UserGroup else UserGroup.objects.get(id = group_id)
    admin = group.admin.email
    id_ = group.id
    link = '/user/add-to-group/' + str(id_) + "/" + md5(str(admin).encode()).hexdigest()
    return link

def get_user_add_group_link(user, group_type):
    group_id = get_user_group(user, group_type)
    if user != group_id.admin.email: return None
    logger.debug(f"group id for generating link : {group_id}")
    return generate_group_add_link(group_id)

def get_group(group_id):
    return group_id if type(group_id) == UserGroup else UserGroup.objects.get(id = group_id)

def get_group_type_object(type_name):
    if isinstance(type_name, str):
        return UserGroupType.objects.filter(type_name__iexact = type_name).first()
    if isinstance(type_name, int): 
        return UserGroupType.objects.filter(id = type_name).first()
    if isinstance(type_name, UserGroupType):
        return type_name


def get_max_members_in_group(group_type_name): #group_name is name of group type
    group_type = get_group_type_object(group_type_name)
    return group_type.max_members

def get_user_group(user, group_type, create = False):
    user = get_user_object(user)
    group_type = get_group_type_object(group_type)
    user_groups = UserGroupMapping.objects.filter(user_profile_id = user).values('user_group_id')
    user_group = UserGroup.objects.filter(id__in = user_groups, user_group_type_id = group_type)
    if create and not user_group.exists():
        logger.debug(f"Group with type : {group_type} doesn't exist for user {user} and will be created")
        return UserGroup.objects.create_user_group(group_type, admin=user)
    if not user_group.exists():
        logger.debug(f"Group doesn't exist and will not created due to create : {create}")
        return None
    return user_group.first()
    

def get_group_of_user_from_plan(user, plan, plan_type, group_type, period):
    """
    Returns group object of user subscribe with plan
    Arguments:
        user {AlgonautsUser, str} -- 
        plan {Plan, str} -- 
    """
    user = get_user_object(user)
    groups = get_all_groups_of_user(user).values('user_group_type_id')
    plan_id  = subscriptions.functions.get_plan_id(plan, plan_type, group_type)
    group_type_id = Plan.objects.filter(user_group_type_id__in = groups, id = plan.id).values("user_group_type_id")
    return UserGroup.objects.filter(user_group_type_id__in = group_type_id).last()

    
def validate_group_add_url_slug(group_id:int, hash_:str):
    group = UserGroup.objects.filter(id = group_id).first()
    if md5(str(group.admin.email).encode()).hexdigest() == hash_:
        return True
    return False


def get_user_subs_plans(user):
    user = get_user_object(user)
    
    now = datetime.datetime.now(pytz.timezone('UTC'))

    iGroupType = UserGroupType.objects.get(min_members = 1, max_members = 1 ) # get the individual object from moddles
    eGroupType = UserGroupType.objects.exclude(min_members = 1, max_members = 1) # get rest group types available from model

    user_all_groups = UserGroupMapping.objects.filter(
                            user_profile_id = user, 
                            time_removed__gt = datetime.datetime.now(pytz.timezone('UTC'))
                            ).values(
                                'user_profile_id', 
                                'user_group_id', 
                                'user_group_id__user_group_type_id'
                                ).values('user_group_id') # one user linked with multiple groups

    indivdual =	user_all_groups.filter(
                            user_profile_id=user, 
                            user_group_id__user_group_type_id = iGroupType
                            ).values('user_group_id__user_group_type_id')
    
    group = user_all_groups.filter(
                            user_profile_id=user, 
                            user_group_id__user_group_type_id__in = eGroupType
                            ).values('user_group_id__user_group_type_id') # filter out all groups of profile with non individual group type 
    
    plans = Subscription.objects.filter(
                            user_group_id__in = user_all_groups, 
                            subscription_end__gt = now, 
                            subscription_start__lt = now).values(
                                'plan_id', 
                                'plan_id__user_group_type_id__max_members' , 
                                'plan_id__user_group_type_id__type_name', 
                                'plan_id__plan_name', 
                                'user_group_id', 
                                'plan_id__user_group_type_id', 
                                'subscription_type_id__type_name', 
                                'plan_id__entry_time', 
                                'plan_id__expiry_time', 
                                'plan_id__price_per_month', 
                                'plan_id__price_per_year',
                                'subscription_start',
                                'subscription_end'
                                )

    group_plans = plans.filter(
                            plan_id__user_group_type_id__in = group, 
                            plan_id__entry_time__lt = now, 
                            plan_id__expiry_time__gt = now 
                            )

    indivdual_plans = plans.filter(
                            plan_id__user_group_type_id__in = indivdual, 
                            plan_id__entry_time__lt = now, 
                            plan_id__expiry_time__gt = now
                            )
                            
    return indivdual_plans, group_plans


def get_user_subs_product(user):
    user = get_user_object(user)
    iplan, gplan = get_user_subs_plans(user)
    plans = list(iplan.values('plan_id'))
    plans.extend(gplan.values('plan_id'))
    plans = [plan['plan_id'] for plan in plans]
    products = subscriptions.functions.get_all_products_in_plans(plans)
    return products

@database_sync_to_async
def get_user_subs_product_async(user):
    return [product.product_name for product in get_user_subs_product(user)]

def get_all_users_in_group(group_id):
    group = UserGroup.objects.get(id = group_id) \
                if isinstance(group_id, int) \
                else group_id
    users = UserGroupMapping \
                .objects \
                .filter(
                    user_group_id = group, 
                    time_removed__gt = datetime.datetime.now(pytz.timezone('UTC'))
                    ).values("user_profile_id")
    return AlgonautsUser.objects.filter(id__in = users)

    
def get_all_groups_of_user(user_id):
    user_id = user_id._wrapped if hasattr(user_id,'_wrapped') else user_id
    user = user_id if type(user_id) == AlgonautsUser else UserGroup.objects.get(id = user_id)
    groups = UserGroupMapping.objects.filter(user_profile_id = user, time_removed__gt = datetime.datetime.now(pytz.timezone('UTC'))).values('user_group_id')
    return UserGroup.objects.filter(id__in = groups)


def add_referral_credits(self_uid, referral_code):
    ref_by = AlgonautsUser.objects.get(referral_code=referral_code)
    ref_to = self_uid if type(self_uid) == AlgonautsUser else AlgonautsUser.objects.get(id = self_uid)
    referral_offer_id = (ReferralOffer.objects.filter(offer_active = True).order_by('offer_end').last()) # take the latest and only active offer
    referral_time = datetime.datetime.now(pytz.timezone('UTC'))
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
    link = '/user/refer/user=' + user.referral_code
    return link


def if_referred(user:AlgonautsUser):
    ref = Referral.objects.filter(referred_by = user).exists()
    return ref


def add_feedback(user, subject, product, message):
    user = get_user_object(user)
    recepient = [user.email, EMAIL_HOST_USER]
    subject = subject + " for " + product
    message = "Thank You We have received your Feedback \n" + message
    subscriptions.functions.send_email(user.email, recepient, subject, message)
    UserFeedback.objects.create(email=user, subject = subject, category_name = product, feedback_message=message).save()


def remove_user_from_group(user, group_type, admin):
    user = get_user_object(user)
    group_id = get_user_group(user, group_type)
    if admin == group_id.admin.email:
        logger.debug(f"User admin succefully verified, will remove {user} from group {group_type}")
        UserGroupMapping.objects.delete_user_from_group(user, group_id, admin)
    else:
        logger.debug(f"admin can't be verified, for user group {group_id} admin is : {group_id.admin.email}, but given : {admin}")


def check_password(user, password):
    user = get_user_object(user)
    auth = authenticate(email=user.email, password=password)
    if auth:
        logger.debug("Password verfied successfully")
        return True
    logger.debug(f"Incorrect password provided, can't verify user {user.email}")
    return False

# EDIT section

def contact_no_edit(user, contact_no):
    user = get_user_object(user)
    AlgonautsUser.objects.filter(id = user.id).update(contact_no = contact_no)
    logger.debug(f"contact number changed sucessfully to {contact_no}")

def get_address(user):
    user = get_user_object(user)
    address = Address.objects.filter(email = user).first()
    if address:
        return {
            "line1" : address.line1,
            "line2" : address.line2,
            "city" : address.city,
            "state" : REV_STATE_DICT[address.state],
            "zipcode" : address.zipcode,      
        }
    else:
        return {
            "line1" : "",
            "line2" : "",
            "city" : "",
            "state" : "",
            "zipcode" : "",
        }

def update_address(user, line1, line2, city, state, zipcode):
    user = get_user_object(user)
    exists = Address.objects.filter(email = user)
    state = STATE_DICT[state]
    if not exists.exists():
        Address.objects.create(
            email = user,
            line1 = line1,
            line2 = line2,
            city = city,
            state = state,
            zipcode = zipcode
        )
    else :
        exists.update(
            line1 = line1,
            line2 = line2,
            city = city,
            state = state,
            zipcode = zipcode
        )
        
def toggle_notification(user):
    user = get_user_object(user)
    AlgonautsUser.objects.filter(id = user.id).update(allow_notification = not user.allow_notification)    
    return not user.allow_notification