import users.functions
import json, logging
import threading
import time
import cachetools
import datetime
from collections import Iterable
from channels.db import database_sync_to_async
from worker.utils import DBManager, MercuryCache
from products.models import UserProductFilter, Product
from worker.consumermanager import ConsumerManager

logger = logging.getLogger('worker')

def clear_filter(user, product):
    logger.debug(f"clearing filter for user : {user},  product : {product}")
    product = Product.objects.filter(product_name__iexact = product).first()
    user = users.functions.get_user_object(user)
    UserProductFilter.objects.filter(user_id = user, product_id = product).delete()

def get_user_filter_for_product(user, product):
    product = Product.objects.filter(product_name__iexact = product).first()
    user = users.functions.get_user_object(user)
    logger.debug(f"User : {user} ,, Product : {product}")
    user_product_filter = UserProductFilter.objects.filter(user_id = user, product_id = product).first() 
    logger.debug(f"User product filter for Product : {product} , user : {user} {type(user)} is : {user_product_filter}")
    if not user_product_filter:
        return {
            "call_type" : None,
            "tickers" : None,
            "sides": None,
            "risk_reward": [0, 5], 
            "profit_percentage": [0, 5], 
            "signal_item": None,
        }
    return json.loads(user_product_filter.filter_attributes)

@database_sync_to_async
def get_user_filter_for_product_async(user, product):
    return get_user_filter_for_product(user, product)

def get_product_names_from_groups(groups):
    return list(map(lambda group : group.replace("-", "#"), groups))

@database_sync_to_async
def get_product_names_from_groups_async(groups):
    return list(map(lambda group : group.replace("-", "#"), groups))
    
def get_user_subs_groups(user):
    products = users.functions.get_user_subs_product(user)
    return list(map(lambda product: product.product_name.replace("#", "-").lower(), products))

@database_sync_to_async
def get_user_subs_groups_async(user):
    products = users.functions.get_user_subs_product(user)
    return list(map(lambda product: product.product_name.replace("#", "-").lower(), products))

def filter(user,  data_list, products_filter = None):
    if not type(data_list) == list: return filter(user, [data_list])
    result_data = []
    logger.debug(f"Will apply filter : {products_filter} to data for user : {user} with datalist : {data_list}")
    
    for data in data_list:
        try : 
            call_type = data['dtype']
            product = DBManager().get_product_from_portfolio(data["portfolio_id"])
            user_filter = get_user_filter_for_product(user, product) \
                                if not products_filter or product not in products_filter \
                                else products_filter[product]
            user_filter_call_type = user_filter['call_type']
            if not user_filter_call_type:
                logger.debug(f"User Filter not set.")
                result_data.append(data)
                continue
            if user_filter["tickers"] and  len(user_filter["tickers"]) != 0 and data['ticker'] not in user_filter['tickers']:
                logger.debug(f"Tickers not in User Filter or Filter is not set to none of Filter for Portfolio : {data['portfolio_id']}")
                continue # will not add in data list
            if call_type != 'tick' and  user_filter["sides"] and len(user_filter["sides"]) != 0 and data['signal'].upper() not in user_filter['sides']:
                logger.debug(f"Signal in data is not in User Filer 'sides'  of Portfolio : {data['portfolio_id']}")
                continue # will not add in data list
            if call_type != 'tick' and not (user_filter["profit_percentage"][0] <= data["profit_percent"] <= user_filter["profit_percentage"][1]):
                logger.debug(f"Profit percentage {data['profit_percent']} not according to as specified in filter for Portfolio : {data['portfolio_id']}")
                continue # will not add in data list
            if call_type != 'tick' and not (user_filter["risk_reward"][0] <= data['risk_reward'] <= user_filter["risk_reward"][1]):
                logger.debug(f"Risk Reward : {data['risk_reward']} not according to as specified in filter for Portfolio : {data['portfolio_id']}")
                continue # will not add in data list
            result_data.append(data)
        except Exception as E :
            logger.error(f"{E} Exception Occured while filtering  data {data}:")
    logger.debug(f"Will send : result data == {result_data} to user {user}")
    return result_data        

@database_sync_to_async
def filter_async(user, data_list, products_filter = None):
    return filter(user, data_list, products_filter)

def fetch_calls_for_today_in_thread(*args, **kwargs):
    args[0].extend(DBManager().db_handler.fetch_calls_for_today(*args[2:], **kwargs))

@cachetools.cached(MercuryCache(10, 60))
def fetch_calls_for_today(*args, **kwargs):
    result = []
    logger.debug(f"fetch calls in worker {datetime.datetime.now()}")
    try : 
        now = time.time()
        logger.debug(f"Already connected to db :")
        result = DBManager().get_calls_for_today(*args, **kwargs)
        logger.debug(f"Time required to fetched calls are : {time.time() - now}")
        return result
    except Exception as E:
        logger.error(f"Error occured while fetching data  :  , {E}")

@database_sync_to_async
def fetch_calls_for_today_async(*args, **kwargs):
    return fetch_calls_for_today(*args, **kwargs)


def filter_calls_from_db(user, calls_dict):
    calls = []
    for k, v in calls_dict.items():
        product = DBManager().get_product_from_portfolio(k)
        user_filter = get_user_filter_for_product(user, product)
        logger.debug(f"User Filter for user {user} is {user_filter}")
        user_filter_call_type = user_filter['call_type']
        for data in v: # iterating over calls in each porfolio
            data.update({
                        'signal' : data['signal'] if isinstance(data['signal'], str) else data['signal'].name,
                        'status' : data['status'] if isinstance(data['status'], str) else  data['status'].value, 
                        'time' : data['time'] if isinstance(data['time'], str) else  data['time'].strftime("%m/%d/%Y, %H:%M:%S"), 
                        'active' :data['active_flag'], 
                        'portfolio_id' : k, 
                        'profit_percent' : round(data['profit_percent'], 2)
                        })
            if not user_filter_call_type:
                logger.debug(f"User Filter not set.")
                calls.append(data)
                continue

            try:
                if user_filter["tickers"] and  len(user_filter["tickers"]) != 0 and data['ticker'] not in user_filter['tickers']:
                    logger.debug(f"Tickers not in User Filter or Filter is not set to none of Filter for Portfolio : {data['portfolio_id']}")
                    continue # will not add in data list
                if user_filter["sides"] and len(user_filter["sides"]) != 0 and data['signal'].upper() not in user_filter['sides']:
                    logger.debug(f"Signal in data is not in User Filer 'sides'  of Portfolio : {data['portfolio_id']}")
                    continue # will not add in data list
                if not (user_filter["profit_percentage"][0] <= data["profit_percent"] <= user_filter["profit_percentage"][1]):
                    logger.debug(f"Profit percentage {data['profit_percent']} not according to as specified in filter for Portfolio : {data['portfolio_id']}")
                    continue # will not add in data list
                if not (user_filter["risk_reward"][0] <= data['risk_reward'] <= user_filter["risk_reward"][1]):
                    logger.debug(f"Risk Reward : {data['risk_reward']} not according to as specified in filter for Portfolio : {data['portfolio_id']}")
                    continue # will not add in data list
                data.update({'signal' : data['signal'],  'status' : data['status'], 'time' : data['time'], 
                    'active' :data['active_flag'], 'portfolio_id' : k})
                calls.append(data)
            except Exception as E :
                logger.error(f"{E} Exception Occured while filtering  data {data}:")
    logger.debug(f"all calls for user {user} after filtering : {calls}")
    return calls
