import logging
import threading
import users.functions
from channels.db import database_sync_to_async

logger = logging.getLogger('worker')
logger.info(f'Initializing CONSUMER MANAGER on thread {threading.get_ident()}')
console_logger = logging.getLogger('')



class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConsumerManager(metaclass=Singleton):
    PROTFOLIO_MAPPER = {
            'TEST': "mercury-intraday",
            '1': "mercury-intraday",
            '2': "mercury-btst",
            '3': "mercury-positional",
            '4': "mercury-longterm",
        }
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

    @staticmethod
    @database_sync_to_async
    def get_eligible_groups(user):
        products = users.functions.get_user_subs_product(user)
        return list(map(lambda product: product.product_name.replace("#", "-").lower(), products))
       
    @staticmethod
    def get_mapped_group(portfolio_id):
        if type(portfolio_id) == int : portfolio_id = str(portfolio_id)
        logger.debug(f"protfolio id : {portfolio_id} of class type {type(portfolio_id)} : mapped to group : {ConsumerManager.PROTFOLIO_MAPPER[portfolio_id.upper()]}")
        return ConsumerManager.PROTFOLIO_MAPPER[portfolio_id.upper()]


ConsumerManager()
