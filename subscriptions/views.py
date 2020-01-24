from django.shortcuts import render, HttpResponse
from .models import Plan
# Create your views here.
from users.models import UserGroupMapping


def plans(request):
    return render(request, 'subscriptions/plans.html', {'plans' : Plan.objects.all()})

def plan_overview(request, slug):
    return render(request, 'subscriptions/plan_overview.html', {'plan' : Plan.objects.get(plan_name=slug)})

def subscribe(request):
    if request.POST:
        form = Subscription_Form(request.POST)
        if form.is_valid():
            details = form.save()
            grp_id = UserGroupMapping.objects.get(user_profile_id=request.user)
    return HttpResponse("hello")


    # author = models.CharField(User.get_username()) #AUTOMATICALLY STORE USERNAME

