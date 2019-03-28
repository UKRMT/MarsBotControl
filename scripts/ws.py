import time
import datetime
import asyncio
import json
import logging
import websockets
from dictionaryDump import getDictionaryKeys as gdk

logging.basicConfig()

STATE = gdk()   
SUBS=set()

async def notify_state():    
    if SUBS != set():
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        for s in SUBS:
            print(s[1])
            message = json.dumps({'id':s[1],'timestamp':ts,'value':55})
            print(message)
            await asyncio.wait([s[0].send(message)])
    
async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
  #  await register(websocket)
    try:
        while True:
            message = await websocket.recv()
            if message.startswith('subscribe'):
                prop = message.split(' ',1)[1]
                SUBS.add((websocket,prop))
                print('prop is '+prop)
                await notify_state()
                
            elif message.startswith('unsubscribe'):
                prop = message.split(' ',1)[1]
                SUBS.remove((websocket,prop))
                await notify_state()
                
            else:
                print(message)
                data = json.loads(message)
                if data['action'] == 'ping':
                    await notify_state()
                else:
                    logging.error("unsupported event: {}", data)
    except websockets.ConnectionClosed:
        print('connection closed')
        return 


print(json.dumps(STATE))
asyncio.get_event_loop().run_until_complete(websockets.serve(counter, port=1234))
asyncio.get_event_loop().run_forever()
