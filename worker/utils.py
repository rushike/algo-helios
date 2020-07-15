import logging
import psycopg2
import threading
from cachetools import TTLCache, Cache
from algonautsutils.dbhandler import DBConnHandler
from algonautsutils.templates import Singleton
from helios.settings import DATABASES

logger = logging.getLogger('worker')

class DBSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if isinstance(cls, DBManager) and  cls in cls._instances and not cls._instances[cls].db_handler:
            cls._instances[cls] = super(DBSingleton, cls).__call__(*args, **kwargs)
        if cls not in cls._instances:
            cls._instances[cls] = super(DBSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DBManager(metaclass=DBSingleton):
    def __init__(self):
        try : 
            self.db_handler = DBConnHandler(host = DATABASES["janus"]["HOST"], database = DATABASES["janus"]["NAME"], 
                    user = DATABASES["janus"]["USER"], password = DATABASES["janus"]["PASSWORD"], 
                    port = DATABASES["janus"]["PORT"], set_update_hitrate_timer=False)
            logger.debug(f"Database handler opened : {self.db_handler}")
        except : 
            self.db_handler = None

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
    
    def get_calls_for_today(self, portfolio_id):
        try:
            return self.db_handler.get_calls_for_today(portfolio_id)
        except psycopg2.InterfaceError as exc:
            logger.error(f"Cursor closed result not fetched from stored procedure due to exception {exc}")            
            return self.get_calls_for_today(portfolio_id)

    def filter_calls(self, calls_dict):
        calls = []
        for port, calls in calls_dict.items():
            for d in calls:
                d.update(
                            {
                                'signal' : d['signal'].name,  
                                'status' : d['status'].value, 
                                'time' : d['time'].strftime("%m/%d/%Y, %H:%M:%S"), 
                                'active' :d['active'], 
                                'portfolio_id' : port, 
                                'profit_percent' : round(d['profit_percent'], 2)
                            }
                    ) # updates dict to make JSON serializable
            calls.extend(calls)
        logger.debug(f"User Sending the Calls: {len(calls)} {calls}, \ncallsitems : {len(calls)}")
        return calls

    def get_mapped_group(self, portfolio_id):
        if isinstance(portfolio_id, str) : portfolio_id = int(portfolio_id)
        return self.get_group_name_from_portfolio(portfolio_id)

class MercuryCache(TTLCache):
    def __setitem__(self, key, value, cache_setitem=Cache.__setitem__):
        if value: super().__setitem__(key, value)

DBManager()
