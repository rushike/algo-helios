import json
import threading
import logging
import os
import datetime
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from django.contrib.auth.models import AnonymousUser
from worker.consumermanager import ConsumerManager
import worker.functions
import users.functions
from worker.utils import DBManager
import secrets

logger = logging.getLogger('worker')
logger.info(f'Initializing DATA PUBLISHER on {threading.get_ident()} {os.getpid()}')



class DataPublisher(AsyncConsumer):
    """
    A class to manage BROWSER CONNECTIONS
    """

    async def websocket_connect(self, event):
        logger.info(f"Data Publisher Connected: {event}" + f"\nTotal Active Users are {ConsumerManager().total_users()}")
        self.user = self.scope['user'] 
        logger.info(f"User {self.user} connected to Data Publisher.")
        await self.send({
            "type": "websocket.accept",
        })

        # Add users to eligible groups
        self.groups = await ConsumerManager().get_eligible_groups_async(self.user)
        logger.info(f"Eligible groups for user are {self.groups}")
        for group in self.groups:
            await self.channel_layer.group_add(
                group,
                self.channel_name
            )
        # Add User to broadcast group, will be used to publish tick updates
        await self.channel_layer.group_add(
            ConsumerManager().get_broadcast_group(),
            self.channel_name
        )
        products = await users.functions.get_user_subs_product_async(self.user)
        logger.debug(f"User subscribed products : {products}")
        self.products_filter = dict([
                        (prod.lower(), await worker.functions.get_user_filter_for_product_async(self.user, prod)) 
                        for prod in products
                        ])
        logger.debug(f"self products_filter : {self.products_filter}")
        self.users_tickers = set()
        [
            self.users_tickers.update(
                    v['tickers'] 
                    if v and v['tickers'] 
                    else DBManager().get_instruments(DBManager().get_portfolio_from_product(product))
                ) 
            for product, v in self.products_filter.items()
            ]
        logger.debug(f"self user tickers : {self.users_tickers}")

    async def websocket_receive(self, event):
        try:
            user = self.user
            logger.debug(f"Received event [{event}] from a user {user}")
            ConsumerManager().register_new_client_conn(user, self)

        except Exception as ex:
            logger.error(f"Failed to recieve to web-socket for the event {event}, error {ex}")


    async def websocket_disconnect(self, event):
        try:
            await self.send({
                "type": "websocket.close"
            })
            user = self.user
            logger.info(f"Data Publisher disconnected for user {user}, with publisher {self}, event {event}")

            ConsumerManager().deregister_client_conn(user, self)
            # Remove the User from all groups
            for room in self.groups:
                await self.channel_layer.group_discard(
                    room,
                    self.channel_name
                )

            # Remove user from the generic group
            await self.channel_layer.group_discard(
                ConsumerManager().get_broadcast_group(),
                self.channel_name
            )
            
        except Exception as ex:
            logger.error(f"Failed to disconnect to web-socket for the event {event}, exception {ex}")
            # TODO: Should be a way to notify the admin

    async def send_message(self, event):
        user = self.user
        response = event.get('message')
        data = json.loads(response)
        if data['dtype'] == 'signal' : data = await worker.functions.filter_async(user, data, self.products_filter)
        # to this point data may be list of dictionary
        if isinstance(data, dict) and data['dtype'] == 'tick' and data['ticker'] not in self.users_tickers: data = None
        if data:
            logger.info(f"Sending data to client throrugh /channel/ {event}")
            await self.send({
                'type' : 'websocket.send',
                'text' : response
            })   
