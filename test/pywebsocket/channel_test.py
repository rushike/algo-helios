import asyncio
import websocket
import argparse
import time
import json
import random, datetime
import threading

url = "ws://dev.algonauts.in/channel/"


import time

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(30):
            time.sleep(1)
            # ws.send("Hello %d" % i)
        time.sleep(1)
        # ws.close()
        print("thread terminating...")
    threading.Thread(target=  run, args = ()).start()


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
# asyncio.get_event_loop().run_until_complete(test_channel())