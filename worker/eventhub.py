import logging, os, threading, json, copy, threading
from collections.abc import Iterable
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from algonautsutils.templates import Singleton
from algonautsutils.connhandler.eventhubconnect import EventHubConnect, ClientMode
from azure.eventhub import EventHubConsumerClient
from helios.settings import EVENTHUB_CONNECTION_STRING, EVENTHUB_NAME, EVENTHUB
from worker.consumermanager import ConsumerManager
import worker.functions


logger = logging.getLogger('worker')
logger.info(f'Initializing EventHub on {threading.get_ident()} {os.getpid()}, {EVENTHUB}')


class EventHub():
    def __init__(self, conn_str = EVENTHUB_CONNECTION_STRING,
                        eh_name = EVENTHUB_NAME):
        self.conn_str = conn_str
        self.eh_name = eh_name

        self.eventhub = EventHubConnect(
                                self.conn_str, 
                                self.eh_name, 
                                ClientMode.RECEIVER, 
                                self.receive
                                )                            # initiating EventHub object as reciever
        self.eventhub.start_receiver(True, False)            # starting EventHub as reciever 


        # self.eventhub = EventHubConsumerClient.from_connection_string(
        #                     conn_str=EVENTHUB_CONNECTION_STRING,
        #                     consumer_group='$Default',
        #                     eventhub_name=EVENTHUB_NAME,
        #                 )                                      # initiating EventHub object as reciever
        # threading.Thread(target = self.start_receiver).start() # starting EventHub as reciever 
        # self.start_receiver()
        # self.eventhub.start_receiver(True, False)           

        self.channel_layer = get_channel_layer()               # getting channel name

    def start_receiver(self):
        try:
            # with self.eventhub:
            #     self.eventhub.receive(
            #             on_event = self.receive,
            #             on_partition_initialize = self.on_partition_initialize,
            #             on_partition_close = self.on_partition_close,
            #             on_error = self.on_error,
            #             # starting_position="-1",  # "-1" is from the beginning of the partition.
            #     )
            pass
        except Exception:
            print('Stopped receiving.')


    def receive(self,  event):
        """Callback sent to EventHub, which is called on occurrence of any event
        """
        logger.info(f"eventhub receive callback received event : {event}")
        # event = event.body_as_json()        
        # data = event["data"]    
        data = event
        data_type = data.get('dtype')
        # if data_type == 'tick': return
        if not data_type and data_type not in ['tick', 'signal', 'signal_update']: # initial check, dtype must present in dictionary, i.e. {'dtype' : ['tick' | 'signal' | 'signal_update'], ...}
            logger.error(f"Incorrect data [{data}] received")
            return
        
        if data_type == 'signal' or data_type == 'signal_update': # Will send by individual group register of particular portfolio 
            logger.debug(f"signal or signal update recieved {data}")
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
                worker.functions.send_notification_for_signal_or_signal_update(data)                               
        elif data_type == 'tick': # Will send to Broadcast group
            logger.debug(f"tick recieved {data}")
            data_list = [data]
            group_names = ConsumerManager().get_broadcast_group(),

        self.send(data_list, group_names)                    

    def send(self, data_list = [], group_names = []):
        """responsible for sending recieved data to AsynConsumer listening on /channel,
        """
        logger.debug(f"sending messages to datapublisher : {data_list} = {group_names}")        
        if not isinstance(group_names, Iterable):
            return self.send([data_list], [group_names])        
        for i in range(len(data_list)):
            group_name, data = group_names[i], data_list[i]
            logger.debug(f"channel : {self.channel_layer},  group name : {group_name}, data : {data}")
            async_to_sync(self.channel_layer.group_send)(group_name, {
                                                                        "type": 'send.message',
                                                                        'message': json.dumps(data)
                                                                   })  
    
    def on_partition_initialize(self, partition_context):
        # Put your code here.
        print("Partition: {} has been initialized.".format(partition_context.partition_id))


    def on_partition_close(self, partition_context, reason):
        # Put your code here.
        print("Partition: {} has been closed, reason for closing: {}.".format(
            partition_context.partition_id,
            reason
        ))


    def on_error(self, partition_context, error):
        # Put your code here. partition_context can be None in the on_error callback.
        if partition_context:
            print("An exception: {} occurred during receiving from Partition: {}.".format(
                partition_context.partition_id,
                error
            ))
        else:
            print("An exception: {} occurred during the load balance process.".format(error))

eventhub = None 
if EVENTHUB: 
    eventhub = EventHub()
    logger.info(eventhub)