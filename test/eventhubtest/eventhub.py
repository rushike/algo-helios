import asyncio
import websockets
import argparse
import time
import json
import random, datetime
from algonautsutils.connhandler.eventhubconnect import EventHubConnect, ClientMode

parser = argparse.ArgumentParser()
parser.add_argument('--env', dest='env', default='dev', choices=["dev", "prod"], help='Env to be tested')
parser.add_argument('--bulk', dest='bulk', action='store_true', default = True,
                    help='To test bulk send, by default single msg will be sent')
parser.add_argument('--tick', dest='tick', action='store_true',
                    help='Just send the tick data')
parser.add_argument('--signal', dest='signal', action='store_true',
                    help='Just send the tick data')                
parser.add_argument('--max', dest='mrange', type=int, choices=range(1, 1000),
                    help='interger specifing max number of signals or ticks to sent')                

args = parser.parse_args()
print(args)

CONNSTR = "Endpoint=sb://eh-algonautsdev.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=Luh9306fwRWBuS+OA3UFOaVbJKLhWGVEhxQ2P4SMtxU="
NAME = "sysadmin"

URL = "wss://fierce-badlands-56980.herokuapp.com/datalink/"


eventhubsender = EventHubConnect(CONNSTR, NAME, ClientMode.SENDER)

print(eventhubsender.send)

CAT = {"4" : "Longterm", "1" : "Intraday", '3' : "Positional", '2' : "BTST"}
with open("test/instruments.json", "r") as f:
    instruments = json.load(f)

signal_sent = set() # will store data in instrument_tokens 

def get_signal():
    global signal_sent
    global CAT
    global instruments
    # instrument_token =  random.randrange(100000, 100100) if args.inst == 0 else args.inst
    ri = random.choice(instruments)
    status = random.choices(['HIT' , 'MISS' , 'Active' , 'Partial HIT', 'Inactive'], weights=[0.16, 0.16, 0.26, 0.26, 0.16])[0]
    data = {'instrument_token': ri[1], 'ticker': ri[2], 'interval': 'week', 'price': random.randint(0, 1000), 
            'target_price': random.randint(0, 1000), 'stop_loss': random.randint(0, 1000), 'signal': random.choice(['SELL', 'BUY']), 'trade_strategy': 'SuperTrend_Longterm', 
            'algo_category': random.choice(['Longterm', 'Intraday', 'Postitional', 'BTST']), 'signal_time': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 'algo_source': 'STAnalysis', 
            'portfolio_id': random.sample([5, 2, 3, 4], k = random.randint(1, 4)), 'db_fetched': False, 'profit_percent': 50.0, 'ltp': 94.5, 'status': status, 'call_id': ri[1], 
            'dtype': random.choice(['signal', 'signal_update']), 'active': True if status in ['Active', 'Partial HIT'] else False, 'override': False, 'risk_reward': 2 }
    print(data)
    signal_sent.add(ri[1])
    return data

def get_ticks():
    global instruments
    if signal_sent == []: time.sleep(3)
    ri = random.choice(signal_sent)
    data = {"dtype": "tick", "last_price": random.randint(0, 1000), "instrument_token":  ri[1], "ticker": ri[2]}
    return data

def send_signal():
    print("sending signal")
    ite = 0
    while args.bulk:
        data = get_signal()
        eventhubsender.send(data)
        ite += 1
        if ite >= args.mrange:
            if input("Do you want to exit. Y/n : " ) == 'Y':
                break
            ite = 0

def send_ticks():
    print("sending ticks")
    ite = 0
    while args.bulk:
        data = get_ticks()
        eventhubsender.send(data)
        ite += 1
        if ite >= args.mrange:
            if input("Do you want to exit. Y/n") == 'Y':
                break
            ite = 0


if args.signal: send_signal()
if args.tick : send_ticks()