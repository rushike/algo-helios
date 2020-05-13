import logging, os, threading, json, copy, threading
from collections.abc import Iterable
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from algonautsutils.templates import Singleton
from algonautsutils.connhandler.eventhubconnect import EventHubConnect, ClientMode
from helios.settings import EVENTHUB_CONNECTION_STRING, EVENTHUB_NAME, EVENTHUB
from worker.consumermanager import ConsumerManager
import worker.functions


logger = logging.getLogger('worker')
logger.info(f'Initializing EventHub on {threading.get_ident()} {os.getpid()}')


class EventHub(metaclass = Singleton):
    def __init__(self, conn_str = EVENTHUB_CONNECTION_STRING,
                        eh_name = EVENTHUB_NAME):
        self.conn_str = conn_str
        self.eh_name = eh_name

        self.eventhub = EventHubConnect(
                                self.conn_str, 
                                self.eh_name, 
                                ClientMode.RECEIVER, 
                                self.receive
                                )                              # initiating EventHub object as reciever
        self.eventhub.start_receiver(True, False)              # starting EventHub as reciever 

        self.channel_layer = get_channel_layer()               # getting channel name

    def receive(self, event):
        """Callback sent to EventHub, which is called on occurrence of any event
        """
        logger.info(f"eventhub receive callback received event : {event}")
        data = event["data"]            
        data_type = data.get('dtype')
        if not data_type and data_type not in ['tick', 'signal', 'signal_update']: # initial check, dtype must present in dictionary, i.e. {'dtype' : ['tick' | 'signal' | 'signal_update'], ...}
            logger.error(f"Incorrect data [{data}] received")
            return
        
        if data_type == 'signal' or data_type == 'signal_update': # Will send by individual group register of particular portfolio 
            logger.debug(f"signal or signal update recieved {data}")
            worker.functions.send_notification_for_signal_or_signal_update(data)
            signal, portfolio_ids = data.get('signal'), data.get('portfolio_id')
            if signal and portfolio_ids and signal not in ('WAIT', 'EXIT'):                
                data_list = []
                group_names = []
                for portfolio_id in portfolio_ids:
                    if portfolio_id == 1: continue
                    datax = copy.deepcopy(data)
                    datax["portfolio_id"] = portfolio_id 
                    group_names.append(ConsumerManager().get_mapped_group(portfolio_id))
                    data_list.append(datax)                                
        elif data_type == 'tick': # Will send to Broadcast group
            logger.debug(f"tick recieved {data}")
            data_list = data
            group_names = ConsumerManager().get_broadcast_group(),

        self.send(data_list, group_names)                    

    def send(self, data = [], group_names = []):
        """responsible for sending recieved data to AsynConsumer listening on /channel,
        """
        logger.debug(f"sending messages to datapublisher : {data} = {group_names}")
        logger.debug("second line")
        if not isinstance(group_names, Iterable) and not isinstance(data, Iterable):
            logger.debug(f"stuck with if")
            return self.send([data], [group_names])        
        logger.debug(f"before for loop")
        for group_name, data in zip(group_names, data):
            logger.debug(f"channel : {self.channel_layer},  group name : {group_name}, data : {data}")
            async_to_sync(self.channel_layer.group_send)(group_name, {
                                                                        "type": 'send.message',
                                                                        'message': json.dumps(data)
                                                                   })  
eventhub = None 
if EVENTHUB: 
    eventhub = EventHub()
    logger.info(f"Event hub initialize object : {eventhub}")
