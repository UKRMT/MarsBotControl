import time
from  datetime import datetime
import asyncio
import json
import websockets
from dict_helper import state_from_openmct_dict as new_state
from DriveControl import DriveControl

STATE = new_state()   
SUBS = set()
DRIVE = DriveControl()

class MessageHub:
    def __init__(self):
        asyncio.get_event_loop().run_until_complete(websockets.serve(self.counter, port=1234))
        asyncio.get_event_loop().run_forever()
        
    async def notify_state(self):    
        if SUBS != set():
            
            ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
            for s in SUBS:
                print(s[1])
                message = json.dumps({'id':s[1],'timestamp':ts,'value':STATE[s[1]]})
                print(message)
                await asyncio.wait([s[0].send(message)])
    
    async def counter(self,websocket, path):
        # register(websocket) sends user_event() to websocket
        #  await register(websocket)
        try:
            while True:
                message = await websocket.recv()
                if message.startswith('subscribe'):
                    prop = message.split(' ',1)[1]
                    SUBS.add((websocket,prop))
                    await self.notify_state()
                    
                elif message.startswith('unsubscribe'):
                    prop = message.split(' ',1)[1]
                    SUBS.remove((websocket,prop))
                    await self.notify_state()
                    
                else:
                    print(message)
                    data = json.loads(message)
                    for key in data:
                        STATE[key]=data[key]
                        if key.startswith('control'):
                            motor = key.split('.')[1]
                            if motor=='motor1speed':
                                DRIVE.moveM1(STATE[key])
                            elif motor=='motor2speed':
                                DRIVE.moveM2(STATE[key])
                            elif motor=='motor3speed':
                                DRIVE.moveM3(STATE[key])
                            elif motor=='motor4speed':
                                DRIVE.moveM4(STATE[key])

                    await self.notify_state()

        except websockets.ConnectionClosed:
            print('connection closed')
            return
