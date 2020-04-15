import logging
from cachetools import TTLCache, Cache
from algonautsutils.dbhandler import DBConnHandler
from algonautsutils.templates import Singleton
from helios.settings import DATABASES
import worker.functions

logger = logging.getLogger('worker')


class DBManager(metaclass=Singleton):
    def __init__(self):
        self.db_handler = DBConnHandler(host = DATABASES["janus"]["HOST"], database = DATABASES["janus"]["NAME"], 
                user = DATABASES["janus"]["USER"], password = DATABASES["janus"]["PASSWORD"], 
                port = DATABASES["janus"]["PORT"], autocommit=False, set_update_hitrate_timer=False)
        logger.debug(f"Database handler opened : {self.db_handler}")

        self.portfolios = dict(self.db_handler.get_portfolios())  # int --> str
        self.reverse_portfolios = dict([(v.lower(), k) for k, v in self.portfolios.items()]) # key are in lower case, str --> int
        self.instruments = dict([(k, self.get_instruments_from_db(k)) for k in self.portfolios]) # instruments dict initialize once.

    def get_instruments_from_db(self, protfolio_id):
        return list(v[0] for v in self.db_handler.get_instruments_from_portfolios(portfolios=[self.portfolios.get(protfolio_id, "Nifty50")])) 

    def get_instruments(self, portfolio_id):
        if isinstance(portfolio_id, str):
            portfolio_id = self.reverse_portfolios.get(portfolio_id.lower(), 'intraday')
        return self.instruments.get(portfolio_id, self.instruments[1])

    def get_portfolio_from_group(self, name:str):
        if isinstance(name, list) or isinstance(name, tuple):
            return [self.reverse_portfolios.get(group.split("-")[1].lower(), 2) for group in name]
        return self.reverse_portfolios.get(name.split("-")[1].lower(), 2) # default portfolio as Intraday

    def get_portfolio_from_product(self, name:str):
        if isinstance(name, list) or isinstance(name, tuple):
            return [self.get_portfolio_from_product(group) for group in name]
        return self.reverse_portfolios.get(name.split("#")[1].lower(), 2) # default portfolio as Intraday
    
    def get_group_name_from_portfolio(self, name):
        if isinstance(name, list) or isinstance(name, tuple):
            return [self.get_product_from_portfolio(id) for id in name]
        if isinstance(name, int): name = self.portfolios.get(name, "intraday")
        return "-".join(["mercury", name.lower()])
        
    def get_product_from_portfolio(self, name):
        if isinstance(name, list) or isinstance(name, tuple):
            return [self.get_product_from_portfolio(id) for id in name]
        if isinstance(name, int): name = self.portfolios.get(name, "intraday")
        return "#".join(["mercury", name])
    
    def filter_calls_from_db(self, user, calls_dict):
        calls = []
        for k, v in calls_dict.items():
            product = DBManager().get_product_from_portfolio(k)
            user_filter = worker.functions.get_user_filter_for_product(user, product)
            user_filter_call_type = user_filter['call_type']
            if not user_filter_call_type:
                logger.debug(f"User Filter not set.")
                [d.update({'signal' : d['signal'] if isinstance(d['signal'], str) else d['signal'].name,
                    'status' : d['status'] if isinstance(d['status'], str) else  d['status'].value, 
                    'time' : d['time'] if isinstance(d['time'], str) else  d['time'].strftime("%m/%d/%Y, %H:%M:%S"), 
                    'active' :d['active_flag'], 'portfolio_id' : k}) for d in v]
                calls.extend(v)
                continue
            for data in v: # iterating over calls in each porfolio
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
                    data.update({'signal' : data['signal'].name,  'status' : data['status'].value, 'time' : data['time'].strftime("%m/%d/%Y, %H:%M:%S"), 
                        'active' :data['active_flag'], 'portfolio_id' : k})
                    calls.append(data)
                except Exception as E :
                    logger.error(f"{E} Exception Occured while filtering  data {data}:")
        logger.debug(f"all calls for user {user} after filtering : {calls}")
        return calls

    def filter_calls(self, calls_dict):
        calls = []
        [[d.update({'signal' : d['signal'].name,  'status' : d['status'].value, 'time' : d['time'].strftime("%m/%d/%Y, %H:%M:%S"), 
                'active' :d['active_flag'], 'portfolio_id' : port}) for d in calls] for port, calls in calls_dict.items()] # updates dict to make JSON serializable
        [calls.extend(v) for _, v in calls_dict.items()]
        logger.debug(f"User Sending the Calls: {len(calls)} {calls}, \ncallsitems : {len(calls)}")
        return calls

    def get_mapped_group(self, portfolio_id):
        if isinstance(portfolio_id, str) : portfolio_id = int(portfolio_id)
        return self.get_group_name_from_portfolio(portfolio_id)

class MercuryCache(TTLCache):
    def __setitem__(self, key, value, cache_setitem=Cache.__setitem__):
        if value: super().__setitem__(key, value)