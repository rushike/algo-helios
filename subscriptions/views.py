from django.shortcuts import render, HttpResponse
from users.models import UserGroupMapping, UserGroup, UserGroupType
from django.db.models import query
from subscriptions.models import Plan, Subscription
import datetime

def plans(request):
    return render(request, 'subscriptions/plans.html', {'plans' : Plan.objects.all()})

def plan_overview(request, slug):
    return render(request, 'subscriptions/plan_overview.html', {'plan' : Plan.objects.get(plan_name=slug)})

def plan_subscribe(request):
    subs_attr = dict(request.POST.lists()) 
    subs_attr['email'] = request.user.email #get users email
    ru = request.user
    # user_plan is an array type
    user_plan = Plan.objects.filter(plan_name=subs_attr['plan_name'][0])[0] 

    #one user linked with multiple groups
    # user_all_groups = UserGroupMapping.objects.filter(user_profile_id=request.user)
    

    ne = UserGroup.objects.create_user_group(user_plan.user_group_type_id, datetime.datetime.now(), admin=request.user)
    ugti = user_plan.user_group_type_id.id
    usermpa = UserGroupMapping.objects.all()
    u_gid_____ = UserGroupMapping.objects.all().values('user_group_id','user_profile_id','user_group_id__user_group_type_id') 
    u_gid = u_gid_____.filter(user_profile_id=request.user, user_group_id__user_group_type_id=user_plan.user_group_type_id)

    u_g = UserGroup.objects.get(id=u_gid[0])
    # import logging
    # import logging.config
    
    # logging.config.fileConfig('logging.conf')
    # logger = logging.getLogger('applog')
    # logger.debug(str(u_gid)+"prit")

    # print(u_gid)

    # for i in range(user_all_groups.count()):
        
    #     if user_all_groups[i].user_group_id.user_group_type_id == user_plan.user_group_type_id:
    #         u_gid = user_all_groups[i].user_group_id
    #         break
    
    
    # saving all the stuff 

    Subscription.objects.create(
        user_group_id = u_g,
        plan_id = user_plan,
        subscription_start = datetime.datetime.now(),
        subscription_end = datetime.datetime.now() + datetime.timedelta(days=1),
        subscription_active = True,
        payment_id = 0, 
    ).save()
    
    return HttpResponse(u_gid)



