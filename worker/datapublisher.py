import json
import threading
import logging
import os
from worker.consumermanager import ConsumerManager
from channels.consumer import AsyncConsumer
from algonautsutils.dbhandler import DBConnHandler


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

        await self.send({
            "type": "websocket.accept",
        })

        # Add users to eligible groups
        for group in ConsumerManager().get_eligible_groups(self.scope['user']):
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
            user = self.scope['user']
            logger.debug(f"Received event [{event}] from a user {user}")

            ConsumerManager().register_new_client_conn(user, self)
            all_calls = DBConnHandler().fetch_calls_for_today()
            await self.send({
                # Send existing table to the client
                "type": "websocket.send",
                "text": json.dumps(ConsumerManager().filter_calls(all_calls, user))
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
