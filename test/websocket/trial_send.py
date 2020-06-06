# Generates random data to send over websocket connection
"""
Function gen_signal() generates signal data and function gen_tick() generates tick data.
The data is generated randomly.
Function send_signal() sends the data over websocket to the webpage present at the uri.
send_signal() keeps sending data until it is stopped by a keyboard interrupt.
The uri is set to localhost and should be configured while running on other than localhost.
"""


import asyncio
import websockets
import argparse
import time
import json
import random, datetime

instrument_tokens = {}

parser = argparse.ArgumentParser()
parser.add_argument('--env', dest='env', default='dev', choices=["dev", "prod"], help='Env to be tested')
parser.add_argument('--address', dest='address', help='Custom web-socket address to be tested')
parser.add_argument('--bulk', dest='bulk', action='store_true',
                    help='To test bulk send, by default single msg will be sent')
parser.add_argument('--tick', dest='tick', action='store_true',
                    help='Just send the tick data')
parser.add_argument('--custom', dest='custom', action='store_true',
                    help='custom send signal')

parser.add_argument('--action', dest='action', default='BUY', choices=["BUY", "SELL"], help='Signal action BUY or SELL')

parser.add_argument('--cat', dest='cat', default='intraday', choices=["intraday", "btst", 'positional', 'longterm'], help='Signal Algorithm Category like ["intraday", "btst", "positional", "longterm"]')

parser.add_argument('--inst', dest='inst', default="0", choices=["0", "1", "2", "3", "4", "5"], help='Signal Algorithm Category like ["0", "1", "2", "3", "4", "5"]')

parser.add_argument('--port', dest='port', default='1', choices=["4", "1", '2', '3'], help='Signal Algorithm Category like [1, 2, 3, 4]')

parser.add_argument('--status', dest='status', default='Active', choices=["Active", "HIT", 'MISS', 'Inactive', 'Partial HIT'], help='Signal status from [HIT, MISS, Active, Inactive, Partial Hit]')

parser.add_argument('--call', dest='call', default=0, choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"], help='Signal callid < 16')


parser.add_argument('--signal', dest='signal', action='store_true',
                    help='Just send the signal data')

parser.add_argument('--update', dest='update', action='store_true',
                    help='Just send the signal data')

parser.add_argument('--interactive', dest='interactive', action='store_true',
                    help='Interactive mode')

args = parser.parse_args()
args.cat = False
"""

"""
print(args)

CAT = {"4" : "Longterm", "1" : "Intraday", '3' : "Positional", '2' : "BTST"}
with open("test/instruments.json", "r") as f:
    instruments = json.load(f)

signal_sent = [] # will store data in instrument_tokens 

# All calls fetched
async def send_signal(bulk=False):
    if args.env == 'dev':
        url = "ws://localhost:8000/datalink/"
    elif args.env == 'prod':
        url = "wss://www.algonauts.in/datalink/"
    else:
        print(f"Error, not a valid env {args.env}")
        return

    async with websockets.connect(url) as websocket:
        while True:
            if args.custom and not args.tick:
                print('sending signal or signal_update')
                test_data = get_signal()
                data = json.dumps(test_data)            
                await websocket.send(data)
                break
            elif args.custom:
                print("sending tick")
                test_data = get_ticks()
                data = json.dumps(test_data)
                await websocket.send(data)
                break

            if not args.bulk:
                break            
            if args.interactive:
                input("Press for Next Entry . . ")
            
            time.sleep(1)
        

def get_signal():
    global signal_sent
    global CAT
    global instruments
    # instrument_token =  random.randrange(100000, 100100) if args.inst == 0 else args.inst
    ri = random.choice(instruments)
    status = random.choices(['HIT' , 'MISS' , 'Active' , 'Partial HIT', 'Inactive'], weights=[0.01, 0.01, 0.47, 0.48, 0.01])[0]
    data = {'instrument_token': ri[1], 'ticker': ri[2], 'interval': 'week', 'price': random.randint(0, 1000), 
            'target_price': random.randint(0, 1000), 'stop_loss': random.randint(0, 1000), 'signal': random.choice(['SELL', 'BUY']), 'trade_strategy': 'SuperTrend_Longterm', 
            'algo_category': random.choice(['Longterm', 'Intraday', 'Positional', 'BTST']), 'signal_time': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 'algo_source': 'STAnalysis', 
            'portfolio_id': random.sample([5, 2, 3, 4], k = random.randint(1, 4)), 'db_fetched': False, 'profit_percent': 50.0, 'ltp': 94.5, 'status': status, 'call_id': ri[1], 
            'dtype': random.choice(['signal', 'signal']), 'active': True if status in ['Active', 'Partial HIT'] else False, 'override': False, 'risk_reward': 2 }
    print(data)
    if ri not in signal_sent:
        signal_sent.append(ri)
    return data

def get_ticks():
    global signal_sent
    global instruments
    if signal_sent == []: time.sleep(1)
    # ri = random.choice(signal_sent)
    ri = random.choice(instruments)
    data = {
        "dtype" : "tick", 
        "data" : []
    }
    for ri in instruments:
        data["data"].append({"last_price": random.randint(0, 1000), "instrument_token":  ri[1], "ticker": ri[2]})
    # data =  {"dtype": "tick","data" : [{"last_price": random.randint(0, 1000), "instrument_token":  340481, "ticker": "HDFC"}]}
    print(data)
    return data

asyncio.get_event_loop().run_until_complete(send_signal(args.bulk))
