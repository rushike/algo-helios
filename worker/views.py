from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from worker.callfilter import session_filters
from django.contrib.auth.decorators import login_required
import logging

import products.functions

logger = logging.getLogger('worker')

def get_health_status(request):
    return HttpResponse(status=200)


@login_required(login_url='/accounts/login/')
def mercury(request):
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    return render(request, 'worker/datapage.html', {'vapid_key': vapid_key, 'active_tab': "Section1"})

@login_required(login_url='/accounts/login/')
def apply_filters(request):
    GET = request.GET.dict()
    logger.info(f"REQUEST  ==:> {request},\nDATA ==:> {request.GET}, \nDICT ==:> {GET} ")
    call_type = request.GET.get('call_type')
    tickers = request.GET.getlist('tickers')
    sides = request.GET.get('sides')
    risk_reward = tuple(float(v.strip()) for v in request.GET.get('rr_range').split("-"))
    profit_percentage = tuple(float(v.strip()) for v in request.GET.get('pp_range').split("-"))
    signal_time = tuple(float(v.strip()) for v in request.GET.get('signal_time', "0 - 1").split("-")) 
    logger.debug(f"GET data : tickers ==:> {tickers}, call_type ==:> {call_type},  sides ==:> {sides}, \n \
                    risk-reward-range ==:> {risk_reward}, profit percentage range ==:> {profit_percentage}")
    filter_dict = {
        "call_type" : call_type,
        "tickers" : tickers,
        "sides" : sides, 
        "risk_reward" : risk_reward,
        "profit_percentage" : profit_percentage,
        "signal_tiem" : signal_time,

    }
    logger.debug(f"Sending attributes to store or update in database : [ \n\t{request.user._wrapped} , \n\t{'mercury#{}'.format(call_type)}, \n\t{filter_dict}\n]")
    products.functions.add_user_products_filter(user_id = request.user, product_id = "mercury#{}".format(call_type), filter_attributes =  filter_dict)
    return HttpResponse(status=500)

@login_required(login_url='/accounts/login/')
def get_filters(request):
    print("REQUEST  ", request, request.GET['session_id'])
    session_id = request.GET['session_id']
    if session_id in session_filters:
        print("SESSION FILTER ", session_filters[session_id].to_dict())
        return JsonResponse(session_filters[session_id].to_dict(), safe=False)
    return JsonResponse(dict())
