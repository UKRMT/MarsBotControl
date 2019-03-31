'''
Title: Open MCT Sensor Poster
Description:
    This is a websocket that will wait for subscriptions from the OpenMCT client on sensor data. It should
    use the same copy of dictionary.json that the openMCT client has as a key for sending packaged data..
Author: Joshua Ashley

Revision History:
    Josh A. 2019-03-26 - Initial Version
    Josh A. 2019-03-29 - Added sensor dictionary on dictionary.json access from getdictionarykeys
'''

import asyncio
import websockets
import json
import datetime
import time
import _thread
from dict_helper import state_from_openmct_dict as new_state

class SensorsWebSocket():
    thread_dict = {}
    sensor_dict = {}
    '''
    Method: initialize
    Description: initalizes the sensor poster by setting up the dictionary json as an instance accessable array.
    '''
    def __init__(self):
        self.sensor_dict = new_state()
        thread_dict = {}
        start_server = websockets.serve(self.listener, port=1234)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    '''
    Method: listener
    Description: Monitors the socket for a message from openMCT and checks what data the openMCT wants against the dictionary in the instance.
    '''
    async def listener(self, websocket, path):
        try:
            while True:
                sensor_request = await websocket.recv()
                print('got request: ' + sensor_request)
                sensor_array = sensor_request.split(" ")
                
                if sensor_array[0] == 'unsubscribe':
                    #check what mct wants to unsubscribe to and kill that thread
                    if self.thread_dict[sensor_array[1]]:
                        self.thread_dict[sensor_array[1]].exit()
                        self.thread_dict.pop(sensor_array[1])
                elif sensor_array[0] == 'subscribe':
                        #add a thread based on what open mct wants to subscribe to
                        new_thread = _thread.start_new_thread(self.sensor_blast, (websocket, sensor_array[1]))
                        self.thread_dict[sensor_array[1]] = new_thread
                else:
                    print('Looking for either subscribe or unsubscribe, neither was given')
        except websockets.ConnectionClosed:
            for key, thread in self.thread_dict.iteritems():
                thread.exit()
                self.thread_dict.pop(key)
                print('Connection Closed, threads killed')
#        except e:
#            print('Unexpected Error')
#            print(e)
    '''
    Method: sensor_blast
    Description: Blasts sensor data through the websocket in a readable format by MCT, this will be a thread automatically started and killed
    '''
    def sensor_blast(self, websocket, sensor_type):
        while True:
            try:
                # get sensor data base on sensor type
                # format it to the constraints of dictionary.json
                # push it through the socket connection
                ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                time_num = time.time()
                message = json.dumps({'id':sensor_type,'timestamp':ts,'value':self.sensor_dict[sensor_type]})
                print('sending' +  message)
                websocket.send(message)
                time.sleep(1)
            except:
                print("unexpected sensor key")
                print(self.sensor_dict)
                print(sensor_type)


                
s = SensorsWebSocket()
