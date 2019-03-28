import asyncio
import json
import logging
import websockets
from dictionaryDump import getDictionaryKeys as gdk

logging.basicConfig()

STATE = {'value': 0}

#STATE = gdk()

print(STATE)

class Client:
    def __init__(self,ws):
        self.subs = set()
        self.ws = ws
    def subscribe(self,key):
        if key not in self.subs:
            self.subs.add(key)
    def unsubscribe(self,key):
        if key in self.subs:
            self.subs.remove(key)
    async def notify(self,ts):
        if self.ws:
            for s in self.subs:
                message = json.dumps({'key':s,'timestamp':ts,'value':STATE[s]})
                self.ws.send(message)

                
USERS = set()

users={}
clients={}

def state_event():
    return json.dumps({'type': 'state', **STATE})

def users_event():
    return json.dumps({'type': 'users', 'count': len(USERS)})

async def notify_state():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def notify_users():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    USERS.add(websocket)
    await notify_users()

async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()

async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await websocket.send(state_event())

        while True:
            message = await websocket.recv()
            clientId = hash(websocket)
            if message.startswith('subscribe'):
                prop = message.split(' ',1)[1]
                clients[clientId] = Client(websocket)

                print('prop: '+prop)

                clients[clientId].subscribe(str(prop))

                print('prop is '+users[hash(websocket)])
                
            elif message.startswith('unsubscribe'):
                prop = message.split(' ',1)[1]
                clients[clientId].unsubscribe(prop)

            else:
                data = json.loads(message)
                if data['action'] == 'minus':
                    STATE['value'] -= 1
                    await notify_state()
                elif data['action'] == 'plus':
                    STATE['value'] += 1
                    await notify_state()
                else:
                    logging.error(
                        "unsupported event: {}", data)
    finally:
        await unregister(websocket)


async def consumer_handler(websocket, path):
    async for message in websocket:
        await consumer(message)
        
asyncio.get_event_loop().run_until_complete(websockets.serve(counter, port=1234))
asyncio.get_event_loop().run_forever()
