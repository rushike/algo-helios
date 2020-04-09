import logging
import threading, itertools
import users.functions
from channels.db import database_sync_to_async

from algonautsutils.dbhandler import DBConnHandler
from helios.settings import DATABASES

logger = logging.getLogger('worker')
logger.info(f'Initializing CONSUMER MANAGER on thread {threading.get_ident()}')


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConsumerManager(metaclass=Singleton):
    PROTFOLIO_MAPPER = {
            'PortfolioTest' : 'mercury-btst',
            'TEST': "mercury-intraday",
            '2': "mercury-intraday",
            '3': "mercury-btst",
            '4': "mercury-positional",
            '5': "mercury-longterm",
        }
    PRODUCT_MAPPER = {
        "mercury#intraday" : 2,
        "mercury#btst" : 3,
        "mercury#positional" : 4,
        "mercury#longterm" : 5,
    }
    GROUP_MAPPER = {
        "mercury-intraday" : 2,
        "mercury-btst" : 3,
        "mercury-positional" : 4,
        "mercury-longterm" : 5,
    }
    def __init__(self):
        logger.info("Initializing ConsumerManager!!!!")
        self.BROADCAST_GROUP = "ALL_USERS"
        self.users_conns = dict()
        self.db_handler = DBConnHandler(host = DATABASES["janus"]["HOST"], database = DATABASES["janus"]["NAME"], 
                user = DATABASES["janus"]["USER"], password = DATABASES["janus"]["PASSWORD"], port = DATABASES["janus"]["PORT"], autocommit=False, set_update_hitrate_timer=False)
        logger.debug(f"Database handler opened : {self.db_handler}")

        self.portfolios = dict(self.db_handler.get_portfolios())  # int --> str
        self.reverse_portfolios = dict([(v.lower(), k) for k, v in self.portfolios.items()]) # key are in lower case, str --> int
        self.instruments = dict([(k, self.get_instruments_from_db(k)) for k in self.portfolios]) # instruments dict initialize once.

    def get_instruments_from_db(self, protfolio_id):
        return list(v[0] for v in self.db_handler.get_instruments_from_portfolios(portfolios=[self.portfolios.get(protfolio_id, "Nifty50")])) 

    def init_db_handler(self):
        logger.debug(f"Reinitiated handler self handler deleted : {self.db_handler}, conn : {self.db_handler.conn}, cursor : {self.db_handler.cursor}")
        self.db_handler.connect()
        logger.debug(f"Reinitiated handler opened : {self.db_handler}, conn : {self.db_handler.conn}, cursor : {self.db_handler.cursor}")

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
    
    def user_exceeds_conns(self, user):
        # TODO: Active conns count should be kept in the DB to avoid problems during horizontal scaling
        if len(self.users_conns.get(user, set())) >= 2:
            return True
        return False


    def register_new_client_conn(self, user, conn):
        logger.debug(f"Adding the connnection : {conn} for user : {user}")
        if not self.user_exceeds_conns(user):
            logger.debug(f"Checked the condition Adding the connnection : {conn} for user : {user}")
            self.users_conns.setdefault(user, set()).add(conn)
            return True
        return False

    def deregister_client_conn(self, user, conn):
        self.users_conns.get(user, set()).discard(conn)

    def total_users(self):
        return len(self.users_conns)

    def get_broadcast_group(self):
        return self.BROADCAST_GROUP

    def filter_calls(self, calls_dict):
        calls = []
        [[d.update({'signal' : d['signal'].name,  'status' : d['status'].value, 'time' : d['time'].strftime("%m/%d/%Y, %H:%M:%S"), 
                'active' :d['active_flag'], 'portfolio_id' : port}) for d in calls] for port, calls in calls_dict.items()] # updates dict to make JSON serializable
        [calls.extend(v) for _, v in calls_dict.items()]
        logger.debug(f"User Sending the Calls: {len(calls)} {calls}, \ncallsitems : {len(calls)}")
        return calls

    @database_sync_to_async
    def get_eligible_groups_async(self, user):
        products = users.functions.get_user_subs_product(user)
        return list(map(lambda product: product.product_name.replace("#", "-").lower(), products))
    
    def get_eligible_groups(self, user):
        products = users.functions.get_user_subs_product(user)
        return list(map(lambda product: product.product_name.replace("#", "-").lower(), products))

    def get_mapped_group(self, portfolio_id):
        if isinstance(portfolio_id, str) : portfolio_id = int(portfolio_id)
        return ConsumerManager().get_group_name_from_portfolio(portfolio_id)


ConsumerManager()
