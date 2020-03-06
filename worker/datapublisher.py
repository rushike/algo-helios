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
console_logger = logging.getLogger('')

class DataPublisher(AsyncConsumer):
    """
    A class to manage BROWSER CONNECTIONS
    """
    
    async def websocket_connect(self, event):
        logger.info(f"DATA PUBLISHER Connected: {event}")
        logger.info(f"Total Active Users are {ConsumerManager().total_users()}")
        logger.info(f"User scope {self.scope['user']}")
        config_file = xml.etree.ElementTree.parse('./worker/dbconfig.xml')
        self.db_handler = DBConnHandler(host = DATABASES["default"]["HOST"], database = DATABASES["default"]["NAME"], 
                user = DATABASES["default"]["USER"], password = DATABASES["default"]["PASSWORD"], port = DATABASES["default"]["PORT"])
        logger.debug(f"Database handler opened : {self.db_handler}")

        await self.send({
            "type": "websocket.accept",
        })

        # Add users to eligible groups
        # groups = await database_sync_to_async(ConsumerManager().get_eligible_groups)(self.scope['user'])
        groups = await ConsumerManager.get_eligible_groups(self.scope['user'])
        logger.debug(f"Eligible groups for user are {groups}")
        for group in groups:
            await self.channel_layer.group_add(
                group,
                self.channel_name
            )
        logger.debug(f"Created groups {groups} with channels {self.channel_name}")
        # Add User to broadcast group, will be used to publish tick updates
        await self.channel_layer.group_add(
            ConsumerManager().get_broadcast_group(),
            self.channel_name
        )

    async def websocket_receive(self, event):
        try:
            user = self.scope['user']
            logger.debug(f"Received event [{event}] from a user {user}")

            ConsumerManager().register_new_client_conn(user, self)
            logger.debug(f"Register the new client {user} with {self}")
            logger.debug(f"current directory : {os.listdir()}")
            
            groups = await ConsumerManager.get_eligible_groups(user) # group-name is product name
            
            product_names = await worker.functions.get_product_names_from_groups(groups)

            for product in product_names:
                product_filter = await worker.functions.get_user_filter_for_product_async(user, product)
                logger.debug(f"Product filter for Product {product},  Filter: {product_filter}")

            all_calls = self.db_handler.fetch_calls_for_today()
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
        response = event.get('message') 
        logger.info(f"Sending data to client throrugh /channel/ {event}")
        await self.send({
            'type' : 'websocket.send',
            'text' : response
        })   