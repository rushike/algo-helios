import datetime, pytz
from subscriptions.models import Plan, Subscription


def check_data_consistency():
    now = datetime.datetime.now(pytz.timezone('UTC'))
    # disabling incative plans
    Plan.objects.filter(expiry_time__lt = now).update(is_active = False)
    Plan.objects.filter(entry_time__gt = now).update(is_active = False)
    
    # enabling active plans
    Plan.objects.filter(expiry_time__gt = now).update(is_active = True)
    Plan.objects.filter(entry_time__lt = now).update(is_active = True)

    # disabling expired subscritpion
    subs = Subscription.objects.filter(subscription_end__lt = now).update(subscription_active = False)
    

