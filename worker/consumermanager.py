import logging
import threading
import users.functions

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

    def __init__(self):
        logger.info("Initializing ConsumerManager!!!!")
        self.BROADCAST_GROUP = "ALL_USERS"
        self.users_conns = dict()

    def user_exceeds_conns(self, user):
        # TODO: Active conns count should be kept in the DB to avoid problems during horizontal scaling
        if len(self.users_conns.get(user, 0)) >= 2:
            return True
        return False

    def register_new_client_conn(self, user, conn):
        if not self.user_exceeds_conns(user):
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
    def get_eligible_groups(user):
        console_logger.info("user logged in ==> " + user.email)
        results = {}
        threading.Thread(target = users.functions.get_user_subs_product, args=(user), kwargs = {"results" : results} )
        console_logger.info("subscribed products are ==> " + str(results) )
        return 
        
    @staticmethod
    def get_mapped_group(portfolio_id):
        return portfolio_id


ConsumerManager()
