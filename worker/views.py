from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from webpush import send_group_notification
import worker.functions, users.functions
from django.contrib.auth.decorators import login_required
import logging, json, time

import products.functions

from worker.utils import DBManager
from worker.consumermanager import ConsumerManager

logger = logging.getLogger('worker')

def get_health_status(request):
    return HttpResponse(status=200)


@login_required(login_url='/accounts/login/')
def mercury(request):
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    return render(request, 'worker/datapage.html', {'vapid_key': vapid_key, 'active_tab': "Section1"})

@login_required(login_url='/accounts/login/')
def mercury2(request):
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    return render(request, 'worker/datapage2.html', {'vapid_key': vapid_key, 'active_tab': "Section1"})

@login_required(login_url='/accounts/login/')
def apply_filters(request):
    GET = request.GET.dict()
    logger.info(f"REQUEST  ==:> {request},\nDATA ==:> {request.GET}, \nDICT ==:> {GET} ")
    call_type = request.GET.get('call_type')
    tickers = request.GET.getlist('tickers') # tickers is list of strings
    sides = request.GET.getlist('sides') # sides is list of strings 
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
        "signal_item" : signal_time,

    }
    logger.debug(f"Sending attributes to store or update in database : [ \n\t{request.user._wrapped} , \n\t{'mercury#{}'.format(call_type)}, \n\t{filter_dict}\n]")
    products.functions.add_user_products_filter(user_id = request.user, product_id = "mercury#{}".format(call_type), filter_attributes =  filter_dict)
    return HttpResponse(status=200)

@login_required(login_url='/accounts/login/')
def apply_filters2(request):
    logger.info(f"request.body : {type(request.body)} {request.body}")
    POST = json.loads(request.body.decode('utf-8'))
    call_type = POST.get('portfolio_id')
    tickers = POST.get('tickers') # tickers is list of strings
    sides = POST.get('sides') # sides is list of strings 
    risk_reward = POST.get('risk_reward')
    profit_percentage = POST.get('profit_percentage')
    # signal_time = tuple(float(v.strip()) for v in request.GET.get('signal_time', "0 - 1").split("-")) 
    logger.debug(f"GET data : tickers ==:> {tickers}, call_type ==:> {call_type},  sides ==:> {sides}, \n \
                    risk-reward-range ==:> {risk_reward}, profit percentage range ==:> {profit_percentage}")
    filter_dict = {
        "call_type" : call_type,
        "tickers" : tickers,
        "sides" : sides, 
        "risk_reward" : risk_reward,
        "profit_percentage" : profit_percentage,
        "type" : POST.get("type"),

    }
    logger.debug(f"Sending attributes to store or update in database : [ \n\t{request.user._wrapped} , \n\t{'mercury#{}'.format(call_type)}, \n\t{filter_dict}\n]")
    products.functions.add_user_products_filter(user_id = request.user, product_id = "mercury#{}".format(call_type), filter_attributes =  filter_dict)
    return HttpResponse(status=200)

@login_required(login_url='/accounts/login/')
def get_filters(request):
    logger.debug(f"GET Request : {request.GET}")
    products = [product.product_name for product in users.functions.get_user_subs_product(request.user.email)]
    logger.debug(f"Products filter : {products}")
    dict_list = [worker.functions.get_user_filter_for_product(request.user.email, product) for product in list(products)]
    logger.debug(f"dict_list filter : {dict_list}")
    key_val_dict = {}
    for dl_item in dict_list:
        if dl_item['call_type'] and dl_item['call_type'].lower() in ['intraday', 'btst', 'positional', 'longterm']:
            key_val_dict[dl_item['call_type'].lower()] = dl_item
    logger.info(f"User : {request.user} filter are : {key_val_dict}")
    return JsonResponse(key_val_dict, safe=False)

@login_required(login_url = '/worker/mercury/')
def get_user_channel_groups(request):
    groups = worker.functions.get_user_subs_groups(request.user)
    logger.debug(f"User channel groups are : {groups}.")
    return JsonResponse(groups, safe=False)

@login_required(login_url = '/accounts/login/')
def get_instruments_from_portfolio(request):
    portfolio_id = request.POST.get("portfolio_id", 1)
    instruments = DBManager().get_instruments(portfolio_id)
    return JsonResponse(instruments, safe= False)

@login_required(login_url = '/accounts/login/')
def get_instruments_for_portfolios(request):
    all_instruments = {}
    for p in range(2, 6):
        instruments = DBManager().get_instruments(p)
        all_instruments[p] = instruments
    return JsonResponse(all_instruments, safe= False)

@login_required(login_url = '/accounts/login/')
def get_calls_from_db(request):
    user = request.user.email
    portfolios = request.POST.getlist("portfolio_id[]", ['intraday', 'btst', 'positional' , 'longterm'])
    portfolios = list(map(lambda value : 'mercury-' + value, portfolios))    
    groups = ConsumerManager().get_eligible_groups(user) # group-name is product name

    groups = list(set(groups).intersection(portfolios))
    product_names =  worker.functions.get_product_names_from_groups(groups)
    all_calls = {}
    user_portfolios = DBManager().get_portfolio_from_group(groups)
    logger.debug(f"user subscribed products : {product_names}, and protfolios : {user_portfolios}")
    for i, product in enumerate(product_names):
        portfolio_id = DBManager().get_portfolio_from_product(product)
        now = time.time()
        calls = worker.functions.fetch_calls_for_today(portfolio_id= portfolio_id)
        logger.debug(f"time required to fetch through cache or db : {time.time() - now}\n \
            calls for portfolio {portfolio_id}, calls : {calls}")
        logger.debug(f"calls for portfolio {portfolio_id}, calls : {calls}")
        all_calls[portfolio_id] = (calls)
    subs_active = True if len(worker.functions.get_user_subs_groups(request.user)) else False
    return JsonResponse({'calls' : worker.functions.serialize_data( all_calls), 'subs-active' : subs_active}, safe= False)

@login_required(login_url = '/accounts/login/')
def get_calls_from_db2(request):
    user = request.user.email
    portfolios = json.loads(request.body.decode('utf-8')).get("portfolio_id", ['intraday', 'btst', 'positional' , 'longterm'])    
    portfolios = list(map(lambda value : 'mercury-' + value, portfolios))    
    groups = ConsumerManager().get_eligible_groups(user) # group-name is product name

    groups = list(set(groups).intersection(portfolios))
    product_names =  worker.functions.get_product_names_from_groups(groups)
    all_calls = {}
    user_portfolios = DBManager().get_portfolio_from_group(groups)
    logger.debug(f"user subscribed products : {product_names}, and protfolios : {user_portfolios}")
    for i, product in enumerate(product_names):
        portfolio_id = DBManager().get_portfolio_from_product(product)
        now = time.time()
        calls = worker.functions.fetch_calls_for_today(portfolio_id= portfolio_id)
        logger.debug(f"time required to fetch through cache or db : {time.time() - now}\n \
            calls for portfolio {portfolio_id}, calls : {calls}")
        logger.debug(f"calls for portfolio {portfolio_id}, calls : {calls}")
        all_calls[portfolio_id] = (calls)
    subs_active = True if len(worker.functions.get_user_subs_groups(request.user)) else False    
    return JsonResponse({'calls' : worker.functions.serialize_data(all_calls), 'subs-active' : subs_active}, safe= False)

@login_required(login_url = '/accounts/login/')
def clear_filter(request):
    portfolio_id = request.POST.get("portfolio_id", 1)
    product = DBManager().get_product_from_portfolio(portfolio_id)
    logger.debug(f"calling worker function filter for portfolio : {portfolio_id}, product : {product}")
    worker.functions.clear_filter(request.user.email, product)
    return HttpResponse("ok")

@login_required(login_url = '/accounts/login/')
def clear_filter2(request):
    portfolio_id = json.loads(request.body.decode('utf-8')).get("portfolio_id", 1)
    product = DBManager().get_product_from_portfolio(portfolio_id)
    logger.debug(f"calling worker function filter for portfolio : {portfolio_id}, product : {product}")
    worker.functions.clear_filter(request.user.email, product)
    return HttpResponse("ok")    
