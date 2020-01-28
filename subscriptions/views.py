from django.shortcuts import render, HttpResponse
from .models import Plan
# Create your views here.
from users.models import UserGroupMapping, UserGroup, UserGroupType
from django.db.models import query

def plans(request):
    return render(request, 'subscriptions/plans.html', {'plans' : Plan.objects.all()})

def plan_overview(request, slug):
    return render(request, 'subscriptions/plan_overview.html', {'plan' : Plan.objects.get(plan_name=slug)})

def plan_subscribe(request):
    subs_attr = dict(request.POST.lists())
    subs_attr['email'] = request.user.email
    user_plan = Plan.objects.filter(plan_name=subs_attr['plan_name'])



    #below : one user linked with multiple groups
    user_all_groups = UserGroupMapping.objects.filter(user_profile_id=request.user)
    
    #below:  a user goes only one group on basis of plan
    
    # interm = UserGroupMapping.objects.select_related('user_group_type_id') 

    # user_select_group = user_all_groups.filter(group_type='')

    # use = UserGroupMapping.objects.select_related('user_group_id').select_related('user_profile_id')

    #below:  a user goes only one group on basis of plan
    # user_final_group = use.filter(user_profile_id=request.user, user_group_type_id=user_plan.user_group_type_id)

    return HttpResponse(usgid)
