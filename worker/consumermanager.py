import logging
import threading, itertools
import users.functions
from channels.db import database_sync_to_async

from worker.utils import DBManager
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
    
    def __init__(self):
        logger.info("Initializing ConsumerManager!!!!")
        self.BROADCAST_GROUP = "ALL_USERS"
        self.users_conns = dict()

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
                'active' :d['active'], 'portfolio_id' : port}) for d in calls] for port, calls in calls_dict.items()] # updates dict to make JSON serializable
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
        return DBManager().get_group_name_from_portfolio(portfolio_id)


ConsumerManager()
