import xml.etree.ElementTree
import json
import threading
import logging
import os
import datetime

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
import channels.layers

from algonautsutils.dbhandler import DBConnHandler

from helios.settings import DATABASES
from worker.consumermanager import ConsumerManager
import worker.functions

logger = logging.getLogger('worker')
logger.info(f'Initializing DATA PUBLISHER on {threading.get_ident()} {os.getpid()}')


class DataPublisher(AsyncConsumer):
    """
    A class to manage BROWSER CONNECTIONS
    """

    async def websocket_connect(self, event):
        logger.info(f"DATA PUBLISHER Connected: {event}")
        logger.info(f"Total Active Users are {ConsumerManager().total_users()}")
        logger.info(f"User scope {self.scope['user']}")
        self.db_handler = DBConnHandler(host = DATABASES["janus"]["HOST"], database = DATABASES["janus"]["NAME"], 
                user = DATABASES["janus"]["USER"], password = DATABASES["janus"]["PASSWORD"], port = DATABASES["janus"]["PORT"])
        logger.debug(f"Database handler opened : {self.db_handler}")

        await self.send({
            "type": "websocket.accept",
        })

        # Add users to eligible groups
        groups = await ConsumerManager.get_eligible_groups(self.scope['user'])
        logger.debug(f"Eligible groups for user are {groups}")
        for group in groups:
            await self.channel_layer.group_add(
                group,
                self.channel_name
            )
        logger.debug(f"Created groups {groups} with on channels {self.channel_name}")
        # Add User to broadcast group, will be used to publish tick updates
        await self.channel_layer.group_add(
            ConsumerManager().get_broadcast_group(),
            self.channel_name
        )

    async def websocket_receive(self, event):
        try:
            user = self.scope['user'].email
            logger.debug(f"Received event [{event}] from a user {user}")
            ConsumerManager().register_new_client_conn(user, self)
            
            groups = await ConsumerManager.get_eligible_groups(user) # group-name is product name
            product_names = await worker.functions.get_product_names_from_groups_async(groups)
            all_calls = []
            user_protfolios = [ k for k, v in  ConsumerManager.PROTFOLIO_MAPPER.items() if v in groups]
            for product in product_names:
                portfolio_id = ConsumerManager.PRODUCT_MAPPER[product]
                product_filter = await worker.functions.get_user_filter_for_product_async(user, product)
                logger.debug(f"Product Filter protfolio {portfolio_id} from worker.functions : {product_filter}")
                if product_filter['call_type']:
                    logger.debug(f"Async Product filter for Product {product}, Portfolio : {portfolio_id}, Filter: {product_filter}, \
                     porfit_percentage {product_filter['profit_percentage']}, type(product_filter['profit_percentage'][0]), \
                     {type(product_filter['profit_percentage'][1])}")
                    tickers = product_filter["tickers"]
                    calls = self.db_handler.fetch_calls_for_today( portfolio_id= portfolio_id, side=product_filter["sides"],
                                    min_risk_reward=product_filter["risk_reward"][0], max_risk_reward=product_filter["risk_reward"][1],
                                min_profit_percent=product_filter["profit_percentage"][0], max_profit_percent=product_filter["profit_percentage"][1])
                    logger.debug(f"calls for protfolio {portfolio_id}  and side : {product_filter['sides']} tickers : {tickers}  is : {calls}")
                else : 
                    calls = self.db_handler.fetch_calls_for_today(portfolio_id= portfolio_id)
                    logger.debug(f"Calls for protfolio {portfolio_id} withoout filter set : calls : = {calls}")
                all_calls.append(calls)

            logger.debug(f"Fetched all calls for today : {all_calls}")

            logger.debug(f"Will send filter data to groups : {groups}")
            await self.send({
                # Send existing table to the client
                "type": "websocket.send",
                "text": json.dumps(ConsumerManager.filter_calls(all_calls, groups))
            })
        except Exception as ex:
            logger.error(f"Failed to connect to web-socket for the event {event}, error {ex}")

    async def websocket_disconnect(self, event):
        try:
            user = self.scope['user']
            logger.info(f"DATA CONSUMER Disconnected for user {user}, event {event}")

            ConsumerManager().deregister_client_conn(user, self)
            await self.send({
                "type": "websocket.close"
            })

            # Remove the User from all groups
            for room in ConsumerManager().get_eligible_groups(self.scope['user']):
                await self.channel_layer.group_discard(
                    room,
                    self.channel_name
                )

            # Remove user from the generic group
            await self.channel_layer.group_discard(
                ConsumerManager().get_broadcast_group(),
                self.channel_name
            )

            logger.info(f"Total Users Connected {ConsumerManager().total_users()}")
        except Exception as ex:
            logger.error(f"Failed to connect to web-socket for the event {event}")
            # TODO: Should be a way to notify the admin

    async def send_message(self, event):
        user = self.scope['user'].email
        logger.debug(f"A user {user}")
        response = event.get('message')
        data = json.loads(response)
        if data['dtype'] == 'signal':data = await worker.functions.filter_async(user, data)
        logger.debug(f"Sending data RESPONE : {data}")
        if data:
            logger.info(f"Sending data to client throrugh /channel/ {event}")
            await self.send({
                'type' : 'websocket.send',
                'text' : response
            })   