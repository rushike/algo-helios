from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required


def get_health_status(request):
    return HttpResponse(status=200)


@login_required(login_url='/accounts/login/')
def mercury(request):
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    return render(request, 'worker/datapage.html', {'vapid_key': vapid_key, 'active_tab': "Section1"})
