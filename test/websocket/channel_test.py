import asyncio
import websocket
import argparse
import time
import json
import random, datetime
import threading
"""
This script can't do login, so you need to require changes in datapublisher regarding scope
by ignoring self.scope['user'], and giving any present email with plans
"""
url = "ws://dev.algonauts.in/channel/"
# url = "ws://localhost:8000/channel/"

count = {}
import time

def on_message(ws, message):
    global count
    count[str(ws)] += 1
    with open('result.json', 'w') as f:
        json.dump(count, f)
        

def on_error(ws, error):
    global count
    print(count)
    print(error)

def on_close(ws):
    global count
    print(count)
    print("### closed ###")

def on_open(ws):
    global count
    count[str(ws)] = 0
    def run(*args):
        # for i in range(30):
        #     time.sleep(1)
            # ws.send("Hello %d" % i)
        ws.send(json.dumps({'load' : True}))
        # time.sleep(1)
        # ws.close()
        print("thread terminating...")
    threading.Thread(target=  run, args = ()).start()


def run_websocket_handler():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    websocket_thread_array = []
    for i in range(2):
        x = threading.Thread(target=run_websocket_handler)
        x.start()
        print("Socket 1 started")
        websocket_thread_array.append(x)
    
    list([x.join() for x in websocket_thread_array])

    print("count : ", count)