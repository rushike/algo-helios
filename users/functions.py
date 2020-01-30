from users.models import AlgonautsUser, UserGroup, UserGroupType, UserGroupMapping
from subscriptions.models import Plan, Subscription
from products.models import Product, ProductCategory, PlanProductMap


def join_to_group(user, group_id): # method add user(self) to the specific group with group_id 
    user_group_id  =group_id if type(group_id) == UserGroup else UserGroup.objects.get(id = group_id)
    mapper = UserGroupMapping.objects.create_user_group_mapping(user_profile_id= user, user_group_id=user_group_id, delta_period=4, group_admin= False)
    return mapper

def get_user_subs_plans(user):
    iGroupType = UserGroupType.objects.get(type_name = 'individual') # get the individual object from moddles
    eGroupType = UserGroupType.objects.exclude(type_name = 'individual') # get rest group types available from model
    #one user linked with multiple groups
    user_all_groups = UserGroupMapping.objects.all().values('user_profile_id', 'user_group_id', 'user_group_id__user_group_type_id').values('user_group_id__user_group_type_id')
    indivdual =	user_all_groups.filter(user_profile_id=user, user_group_id__user_group_type_id = iGroupType).values('user_group_id__user_group_type_id')
    group = user_all_groups.filter(user_profile_id=user, user_group_id__user_group_type_id__in = eGroupType) # filter out all groups of profile with non individual group type 
    
    indivdual_plans = Plan.objects.filter(user_group_type_id__in = indivdual)
    group_plans = Plan.objects.filter(user_group_type_id__in = group)		

    return indivdual_plans, group_plans

def get_user_subs_product(user):
    iplan, gplan = get_user_subs_plans(user)
    iproducts = PlanProductMap.objects.filter(plan_id__in = iplan)
    gproducts = PlanProductMap.objects.filter(plan_id__in = gplan)

    ig_products = list(iproducts)
    igl_products = ig_products.extend(gproducts)

    raise InterruptedError("Checking Variables value") 

def get_all_users_in_group(group_id):
    group = group_id if type(group_id) == UserGroup else UserGroup.objects.get(id = group_id)
    users = UserGroupMapping.objects.filter(user_group_id = group)
    