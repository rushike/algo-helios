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
import json
import random

instrument_tokens = {}

parser = argparse.ArgumentParser()
parser.add_argument('--env', dest='env', default='dev', choices=["dev", "prod"], help='Env to be tested')
parser.add_argument('--address', dest='address', help='Custom web-socket address to be tested')
parser.add_argument('--bulk', dest='bulk', action='store_true',
                    help='To test bulk send, by default single msg will be sent')
parser.add_argument('--tick', dest='tick', action='store_true',
                    help='Just send the tick data')
parser.add_argument('--signal', dest='signal', action='store_true',
                    help='Just send the signal data')
parser.add_argument('--interactive', dest='interactive', action='store_true',
                    help='Interactive mode')

args = parser.parse_args()

"""

"""
print(args)


def gen_signal():
    global instrument_tokens
    instrument_token = random.randrange(100000, 100100)
    # instrument_token = 99999
    ltp = round(random.random() * 1000, 2)
    signal = random.choice(["BUY", "SELL"])
    test_data = {"dtype": "signal",
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
                 "portfolio_id": random.choice([1, 2, 3, 4, "TEST"]) if args.env == 'dev' else 'TEST'
                 # "portfolio_id": 'TEST',
                 }
    instrument_tokens[instrument_token] = test_data
    return test_data


def gen_tick():
    global instrument_tokens
    instrument_token = random.choice(list(instrument_tokens.keys())) if len(instrument_tokens) > 0 \
        else random.randrange(100000, 100100)
    ltp = instrument_tokens[instrument_token]['price']
    test_tick = {"dtype": "tick",
                 "tradable": True,
                 "mode": "ltp",
                 "instrument_token": instrument_token,
                 "last_price": ltp + round((random.random() - 0.5) * 0.02 * ltp, 2),
                 "portfolio_id": random.choice([1, 2, 3, 4, "TEST"]) if args.env == 'dev' else 'TEST',
                 # "portfolio_id": 'TEST',
                 }
    return test_tick


async def send_signal(bulk_send=False):
    if args.env == 'dev':
        url = "ws://localhost:8000/datalink/"
    elif args.env == 'prod':
        url = "wss://www.algonauts.in/datalink/"
    else:
        print(f"Error, not a valid env {args.env}")
        return

    async with websockets.connect(url) as websocket:
        while True:
            if args.tick or args.signal:
                if args.tick:
                    test_tick = gen_tick()
                    data = json.dumps(test_tick)
                    await websocket.send(data)
                elif args.signal:
                    test_data = gen_signal()
                    data = json.dumps(test_data)
                    print('Sending ', data)
                    await websocket.send(data)
            else:
                test_data = gen_signal()
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


asyncio.get_event_loop().run_until_complete(send_signal(args.bulk))
