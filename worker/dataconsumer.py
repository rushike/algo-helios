import threading
import logging
import json, copy
from webpush import send_group_notification
from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from django.contrib.sites.models import Site
from worker.consumermanager import ConsumerManager
import worker.functions


logger = logging.getLogger('worker')
logger.info(f'**** DATA CONSUMER **** {threading.get_ident()}')

DOMAIN = Site.objects.get_current().domain
logger.debug(f"DOMAIN :  {DOMAIN}, URL : {''.join([DOMAIN, '/worker/mercury/'])}")

class DataConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        logger.info(f"Data Consumer Connected: {event}")
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):        
        logger.debug(f"Data Consumer Received: {event}")

        data = json.loads(event['text'])
        data_type = data.get('dtype')
        if not data_type:
            logger.error(f"Incorrect data [{data}] received")
            return

        if data_type == 'signal' or data_type == 'signal_update':
            signal, portfolio_id = data.get('signal'), data.get('portfolio_id')
            logger.debug(f"Signal : {signal}, prortfolio : {portfolio_id}")
            if signal and portfolio_id and signal not in ('WAIT', 'EXIT'):
                # All ratios will be computed in 'janus', so just forward from here based on the permissions
                datax = copy.deepcopy(data)
                logger.info(f"Will send to {len(portfolio_id)} protfolios..")
                for prtf_id in portfolio_id:
                    if prtf_id == 1: continue
                    datax["portfolio_id"] = prtf_id 
                    group_name = ConsumerManager().get_mapped_group(prtf_id)
                    logger.info(f"Received Signal {datax} with portfolio id : {prtf_id} and will send to group {group_name}.")
                    await self.channel_layer.group_send(
                        group_name,
                        {
                            'type': 'send.message',
                            'message': json.dumps(datax)
                        }
                    )
                    await worker.functions.send_notification_for_signal_or_signal_update(data)
            else:
                logger.error(f"Received INCORRECT Signal {data}")
        elif data_type == 'tick':            
            await self.channel_layer.group_send(
                ConsumerManager().get_broadcast_group(),
                {
                    'type': 'send.message',
                    'message': json.dumps(data)
                }
            )

    async def send_message(self, event):
        response = event.get('message') 
        await self.send({
            'type' : 'websocket.send',
            'message' : json.dumps(response)
        })   

    async def websocket_disconnect(self, event):
        logger.info(f"Data Consumer Disconnected: , {event}")
        await self.send({
            "type": "websocket.close"
        })

    
    @database_sync_to_async
    def send_group_notification_async(self, group_name, payload, ttl):
        send_group_notification(group_name = group_name, payload = payload, ttl = ttl)