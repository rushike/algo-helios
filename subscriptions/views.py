from django.shortcuts import render
from .models import Plan
# Create your views here.

def plans(request):
    return render(request, 'subscriptions/plans.html', {'plans' : Plan.objects.all()})

def plan_overview(request):
    return render(request, 'subscriptions/plan_overview.html', {'plan' : Plan.objects.first()})
    