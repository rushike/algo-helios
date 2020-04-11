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
        groups = await ConsumerManager().get_eligible_groups_async(self.user)
        logger.info(f"Eligible groups for user are {groups}")
        for group in groups:
            await self.channel_layer.group_add(
                group,
                self.channel_name
            )
        # Add User to broadcast group, will be used to publish tick updates
        await self.channel_layer.group_add(
            ConsumerManager().get_broadcast_group(),
            self.channel_name
        )

    async def websocket_receive(self, event):
        try:
            user = self.user
            logger.debug(f"Received event [{event}] from a user {user}")
            ConsumerManager().register_new_client_conn(user, self)
        except Exception as ex:
            logger.error(f"Failed to recieve to web-socket for the event {event}, error {ex}")


    async def websocket_disconnect(self, event):
        try:
            user = self.user
            logger.info(f"Data Publisher disconnected for user {user}, event {event}")

            ConsumerManager().deregister_client_conn(user, self)
            await self.send({
                "type": "websocket.close"
            })

            # Remove the User from all groups
            for room in ConsumerManager().get_eligible_groups_async(self.user):
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
        if data['dtype'] == 'signal':data = await worker.functions.filter_async(user, data)
        if data:
            logger.info(f"Sending data to client throrugh /channel/ {event}")
            await self.send({
                'type' : 'websocket.send',
                'text' : response
            })   
