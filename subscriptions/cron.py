import datetime, pytz, logging
from subscriptions.models import Plan, Subscription

logger = logging.getLogger('worker')

logger.info(f"In Corn.py file, registering the functions")

def check_data_consistency():
    now = datetime.datetime.now(pytz.timezone('UTC'))
    logger.debug(f"Running check-data-consitency .. . {now}")
    # disabling incative plans
    Plan.objects.filter(expiry_time__lt = now, entry_time__gt = now).update(is_active = False)
    
    # enabling active plans
    Plan.objects.filter(expiry_time__gt = now, entry_time__lt = now).update(is_active = True)
    
    # disabling expired subscritpion
    subs = Subscription.objects.filter(subscription_end__lt = now).update(subscription_active = False)
    

