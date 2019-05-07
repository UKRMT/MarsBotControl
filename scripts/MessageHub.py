from __future__ import print_function
import time
from  datetime import datetime
import asyncio
import json
import re
import websockets
from dict_helper import state_from_openmct_dict as new_state
from DriveControl import DriveControl
from ActuatorControl import ActuatorControl
from BeltControl import BeltControl

STATE = new_state()
SUBS  = set()
DRIVE = DriveControl()
ACTS = ActuatorControl('/dev/roboclaw3', '/dev/roboclaw5')
BELTS = BeltControl('/dev/roboclaw4')

class MessageHub:
    action_dict = {
        'motor1speed'       : lambda state: DRIVE.moveM1(state),
        'motor2speed'       : lambda state: DRIVE.moveM2(state),
        'motor3speed'       : lambda state: DRIVE.moveM3(state),
        'motor4speed'       : lambda state: DRIVE.moveM4(state),
        'digarmspeed'       : lambda state: ACTS.moveDig(state),
        'raisearmspeed'     : lambda state: ACTS.moveRaise(state),
        'digmotorspeed'     : lambda state: BELTS.dig(state),
        'offloadmotorspeed' : lambda state: BELTS.offload(state)
    }
    current_dict = {
        'sensors.motor1current'      : lambda :DRIVE.readCurrents(0), 
        'sensors.motor2current'      :  lambda :DRIVE.readCurrents(1),
        'sensors.motor3current'      :  lambda :DRIVE.readCurrents(2),
        'sensors.motor4current'      :  lambda :DRIVE.readCurrents(3),
        'sensors.raisearmcurrent'    :  lambda :ACTS.readCurrents(0),
        'sensors.digmotorcurrent'    :  lambda :BELTS.readCurrents(1),
        'sensors.offloadmotorcurrent':  lambda :BELTS.readCurrents(0),
        'sensors.digarmcurrent'      :  lambda :ACTS.readCurrents(1) 
    }
    def __init__(self):
        asyncio.get_event_loop().run_until_complete(websockets.serve(self.counter, port=1234))
        asyncio.get_event_loop().run_forever()

    async def notify_state(self):
        if SUBS != set():
            ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
            for s in SUBS:
                print(s[1])
                if re.match(r'sensors\..*current', s[1]) is not None: 
                    message = json.dumps({'id':s[1],'timestamp':ts, 'value':self.current_dict[s[1]]()})
                else: 
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

                elif message.startswith('unsubscribe'):
                    prop = message.split(' ',1)[1]
                    SUBS.remove((websocket,prop))
                elif message.startswith('ping'):
                    await self.notify_state()
                else:
                    print(message)
                    data = json.loads(message)
                    for key in data:
                        STATE[key]=data[key]
                        if key.startswith('control'):
                            motor = key.split('.')[1]
                            self.action_dict.get(str(motor), lambda state: print("unknown control key " + key))(STATE[key])

        except websockets.ConnectionClosed:
            print('connection closed')
            return
