import datetime, pytz, logging
from subscriptions.models import Plan, Subscription
import users.functions
from webpush.models import  PushInformation
from itertools import chain
logger = logging.getLogger('worker')

logger.info(f"In Corn.py file, registering the functions")

def check_data_consistency():
    now = datetime.datetime.now(pytz.timezone('UTC'))
    logger.debug(f"Running check-data-consitency .. . {now}")
    # disabling incative plans
    Plan.objects.filter(expiry_time__lt = now, entry_time__gt = now).update(is_active = False)
    
    # enabling active plans
    Plan.objects.filter(expiry_time__gt = now, entry_time__lt = now).update(is_active = True)

    # removing webpush info for inactive subscriptions
    subs_groups = Subscription.objects.filter(subscription_end__lt = now).values('user_group_id')
    users_set = set()
    for group in subs_groups:
        for user in users.functions.get_all_users_in_group(group['user_group_id']).values('id'):
            users_set.add(user['id'])
    push_info = PushInformation.objects.filter(user__in =   users_set).delete()

    # disabling expired subscritpion
    Subscription.objects.filter(subscription_end__lt = now).update(subscription_active = False)
    Subscription.objects.filter(subscription_end__gt = now, subscription_start__lt = now).update(subscription_active = True)
    



