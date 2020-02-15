from django.contrib.auth import get_user_model
from django import forms
from subscriptions.models import Plan


class subscription_form(forms.Form):
    @staticmethod
    def total_plans(self):
        all_plans = Plan.objects.filter()
        for x in all_plans:
            print(x)
    