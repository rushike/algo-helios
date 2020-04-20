import logging
from cachetools import TTLCache, Cache
from algonautsutils.dbhandler import DBConnHandler
from algonautsutils.templates import Singleton
from helios.settings import DATABASES

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
    
    def get_calls_for_today(self, portfolio_id):
        try:
            conn = self.db_handler.pool.getconn()
            conn.autocommit = self.db_handler.autocommit
            cur = conn.cursor()
            logger.debug(f"open the cursor for stored procedure : {cur}")
            cur.callproc('get_calls_for_today', [portfolio_id, ])
            result = cur.fetchall()
            logger.debug(f"Fetch from stored procedure : {result}")
            cur.close()
            self.db_handler.pool.putconn(conn)
            result_dict = self.db_handler.generate_call_dict(result, portfolio_id_present = True)
            logger.debug(f"Generated dict for result from stored procedure : {result_dict}")
            return result_dict
        except Exception as exc:
            logger.error(f"Result not fetched for portofolio_id : {portfolio_id} due to exception {exc}")
            cur.close()
            self.db_handler.pool.putconn(conn)


    def filter_calls(self, calls_dict):
        calls = []
        for port, calls in calls_dict.items():
            for d in calls:
                d.update(
                            {
                                'signal' : d['signal'].name,  
                                'status' : d['status'].value, 
                                'time' : d['time'].strftime("%m/%d/%Y, %H:%M:%S"), 
                                'active' :d['active_flag'], 
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