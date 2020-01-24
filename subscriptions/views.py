from django.shortcuts import render, HttpResponse
from .models import Plan
# Create your views here.
from users.models import UserGroupMapping


def plans(request):
    return render(request, 'subscriptions/plans.html', {'plans' : Plan.objects.all()})

def plan_overview(request, slug):
    return render(request, 'subscriptions/plan_overview.html', {'plan' : Plan.objects.get(plan_name=slug)})

def plan_subscribe(request):
    subs_attr = dict(request.POST.lists())
    subs_attr['email'] = request.user.email
    
    return HttpResponse(subs_attr.items())
