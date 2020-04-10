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
class store:
    instruments_list = [] # it contains intruments for which signal is sent
    @classmethod
    def push(cls, value):
        cls.instruments_list.append(value)
        with open('test/pywebsocket/instrument_send.json', 'w') as f:
            json.dump(cls.instruments_list, f)
    @classmethod
    def get(cls):
        with open('test/pywebsocket/instrument_send.json', 'r') as f:
            cls.instruments_list = json.load(f)
    @classmethod
    def empty(cls):
        cls.instruments_list = []
        with open('test/pywebsocket/instrument_send.json', 'w') as f:
            json.dump(cls.instruments_list, f)

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
with open("test/pywebsocket/instruments.json", "r") as f:
    instruments = json.load(f)

def gen_signal():
    global instrument_tokens
    global CAT
    instrument_token =  random.randrange(100000, 100100) if args.inst == 0 else args.inst
    # instrument_token = 99999
    ltp = round(random.random() * 1000, 2)
    signal = random.choice(["BUY", "SELL"])
    test_data = {
                    "dtype": "signal",
                    "instrument_token": instrument_token,
                    "ticker": "TEST_" + "{}".format(random.randrange(1, 9)),
                    # "ticker": "NIFTY BANK",
                    "price": ltp,
                    "trade_life": "-",
                    "target_price": ltp + round(random.random() + (0.5 if signal == 'BUY' else -0.5) * 0.1 * ltp, 2),
                    "stop_loss": ltp + round(random.random() - (0.5 if signal == 'BUY' else -0.5) * 0.1 * ltp, 2),
                    "signal": signal,
                    "signal_time": "-",
                    "algo_source": random.choice(["MACD", "HA"]),
                    "interval": random.choice(["5minute", "15minute"]),
                    "portfolio_id": random.choice([1, 2, 3, 4, "TEST"]) if args.env == 'dev' else 'TEST', 
                 # "portfolio_id": 'TEST',
                 }
    instrument_tokens[instrument_token] = test_data
    return test_data

def gen_new_signal():
    global instrument_tokens
    global CAT
    instrument_token =  random.randrange(100000, 100100) if args.inst == 0 else args.inst
    ltp = round(random.random() * 1000, 2)
    signal = args.action
    status = random.choice(['HIT' , 'MISS' , 'Active' , 'Partial HIT', 'Inactive'])
    status = args.status
    test_data = {
                    "dtype": "signal",
                    "ticker": "TEST_" + "{}".format(args.inst),
                    "instrument_token": instrument_token,
                    "signal": signal,
                    # "ticker": "NIFTY BANK",
                    "ltp" : ltp,
                    "price": ltp,
                    "target_price": ltp + round(random.random() + (0.5 if signal == 'BUY' else -0.5) * 0.1 * ltp, 2),
                    "stop_loss": ltp + round(random.random() - (0.5 if signal == 'BUY' else -0.5) * 0.1 * ltp, 2),
                    'status' : status,
                    'trade_strategy' : "SuperTrend_Longterm",
                    'algo_category' : args.cat if args.cat else CAT[args.port],
                    "trade_life": "-",
                    "algo_source": random.choice(["MACD", "HA"]),
                    "interval": random.choice(["5minute", "15minute"]),
                    "portfolio_id": args.port, #random.choice([1, 2, 3, 4, "TEST"]) if args.env == 'dev' else 'TEST',
                    # "portfolio_id": 'TEST',
                    'call_id': random.randint(1, 16) if args.call == 0 else args.call, # This will be always unique right? If yes, we can use this as an id for table rows
                    'db_fetched': True,
                    'signal_time': '2020-02-10T09:15:00.054006+05:30',
                    'active': True if status in ['Active', 'Partial HIT'] else False,
                    'profit_percent': 10,
                    'risk_reward': 2,
                    'override': False,
                }
    instrument_tokens[instrument_token] = test_data
    return test_data

def signal_update():
    global instrument_tokens
    global CAT
    instrument_token =  random.randrange(100000, 100100) if args.inst == 0 else args.inst
    signal = args.action
    price = round(random.random() * 1000, 2)
    status = args.status
    test_data = {
        'dtype' : "signal_update",
        'ticker': "TEST_" + "{}".format(args.inst),
        'instrument_token': instrument_token,
        'call_id': random.randint(1, 16) if args.call == 0 else args.call,
        'portfolio_id': args.port,
        'status': status,
        'active': True if status in ['Active', 'Partial HIT'] else False, # True if PartialHIT
        'profit_percent': 10, # Percentage profit/loss earned, Need to think about this
        'signal': signal,
        'algo_category': args.cat if args.cat else CAT[args.port],
        'price': price,
    }
    instrument_tokens[instrument_token] = test_data
    return test_data


def gen_tick():
    global instrument_tokens
    global CAT
    instrument_token =  random.randrange(100000, 100100) if args.inst == 0 else args.inst
    ltp = random.randint(300, 10000)
    test_tick = {"dtype": "tick",
                 "tradable": True,
                 "mode": "ltp",
                 "instrument_token": instrument_token,
                 "last_price": ltp + round((random.random() - 0.5) * 0.02 * ltp, 2),
                 'ticker' : "TEST_" + "{}".format(random.randrange(1, 9)),
                 "portfolio_id": random.choice([1, 2, 3, 4, "TEST"]) if args.env == 'dev' else 'TEST',
                 'status': args.status #random.choice(['HIT' , 'MISS' , 'Inactive' , 'PartialHIT', 'Inactive']),
                 # "portfolio_id": 'TEST',
                 }
    return test_tick

# All calls fetched
async def send_signal(bulk_send=False):
    if args.env == 'dev':
        url = "ws://dev.algonauts.in/datalink/"
    elif args.env == 'prod':
        url = "wss://www.algonauts.in/datalink/"
    else:
        print(f"Error, not a valid env {args.env}")
        return

    async with websockets.connect(url) as websocket:
        while True:
            if args.custom and args.tick:
                test_data = send_custom_tick()
                data = json.dumps(test_data)
                print("sending tick")
                await websocket.send(data)
                break
            elif args.custom:
                test_data = send_custom_signal()
                data = json.dumps(test_data)
                print('sending signal or signal_update')
                await websocket.send(data)
                break

            if args.tick or args.signal or args.update:
                if args.tick:
                    test_tick = gen_tick()
                    data = json.dumps(test_tick)
                    await websocket.send(data)
                elif args.signal:
                    test_data = gen_new_signal()
                    data = json.dumps(test_data)
                    print('Sending ', data)
                    await websocket.send(data)
                elif args.update:
                    test_data = signal_update()
                    data = json.dumps(test_data)
                    print('Sending ', data)
                    await websocket.send(data)
                    await asyncio.sleep(1)

            else:
                test_data = gen_new_signal()
                data = json.dumps(test_data)
                print('Sending ', data)
                await websocket.send(data)
                await asyncio.sleep(1)

                test_data = signal_update()
                data = json.dumps(test_data)
                print('Sending ', data)
                await websocket.send(data)
                await asyncio.sleep(1)

                test_tick = gen_tick()
                data = json.dumps(test_tick)
                print('Sending ', data)
                await websocket.send(data)
                await asyncio.sleep(1)
            if not bulk_send:
                break
            if args.interactive:
                input("Press for Next Entry . . ")
        

def send_custom_signal():
    global instrument_tokens
    global CAT
    global instruments
    store.get()
    # instrument_token =  random.randrange(100000, 100100) if args.inst == 0 else args.inst
    ri = random.choice(instruments)
    status = random.choices(['HIT' , 'MISS' , 'Active' , 'Partial HIT', 'Inactive'], weights=[0.16, 0.16, 0.26, 0.26, 0.16])[0]
    data = {'instrument_token': ri[1], 'ticker': ri[2], 'interval': 'week', 'price': random.randint(0, 1000), 
            'target_price': random.randint(0, 1000), 'stop_loss': random.randint(0, 1000), 'signal': random.choice(['SELL', 'BUY']), 'trade_strategy': 'SuperTrend_Longterm', 
            'algo_category': random.choice(['Longterm', 'Intraday', 'Postitional', 'BTST']), 'signal_time': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 'algo_source': 'STAnalysis', 
            'portfolio_id': random.sample([5, 2, 3, 4], k = random.randint(1, 4)), 'db_fetched': False, 'profit_percent': 50.0, 'ltp': 94.5, 'status': status, 'call_id': ri[1], 
            'dtype': random.choice(['signal', 'signal_update']), 'active': True if status in ['Active', 'Partial HIT'] else False, 'override': False, 'risk_reward': 2 }
    # data = {'instrument_token': ri[1], 'ticker': ri[2], 'interval': 'week', 'price': random.randint(0, 1000), 
    #         'target_price': random.randint(0, 1000), 'stop_loss': random.randint(0, 1000), 'signal': random.choice(['SELL', 'BUY']), 'trade_strategy': 'SuperTrend_Longterm', 
    #         'algo_category': 'Intraday', 'signal_time': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 'algo_source': 'STAnalysis', 
    #         'portfolio_id': [2], 'db_fetched': False, 'profit_percent': 50.0, 'ltp': 94.5, 'status': status, 'call_id': ri[1], 
    #         'dtype': random.choice(['signal', 'signal_update']), 'active': True if status in ['Active', 'Partial HIT'] else False, 'override': False, 'risk_reward': 2 }
    print(data)
    store.push(ri)
    return data

def send_custom_tick():
    global instruments
    # store.get()
    # print("instrument list : ", store.instruments_list)
    # if store.instruments_list == []: time.sleep(3)
    # ri = random.choice(store.instruments_list)
    # 340481, "HDFC"]
    # data = {"dtype": "tick", "last_price": random.randint(0, 1000), "instrument_token":  ri[1], "ticker": ri[2]}
    data = {"dtype": "tick", "last_price": random.randint(0, 1000), "instrument_token":  340481, "ticker": "HDFC"}
    print(data)
    return data

asyncio.get_event_loop().run_until_complete(send_signal(args.bulk))
