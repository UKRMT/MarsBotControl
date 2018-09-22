#Wezley Mitchell 9/22/2018
#Test code to send value of joystick to rPi control servo over UDP Sockets
import os
from socket import *
import inputs #inputs is a lightweight gpuless input library (unlike pygame)
import time
import math
host = "192.168.1.13"	#IP of the listener.
port = 5468		#Port to send on
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)

pad = inputs.devices.gamepads

if len(pad) == 0:
    raise Exception("Couldn't find gamepads!")

#the inputs library gives a wide range of values but the servo accepts values
#between ~500 and ~2500. We must scale these to match.
def translate(value, leftMin, leftMax, rightMin, rightMax):
    #Get how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    #Convert Value to range between 0 and 1
    valueScaled = float(value - leftMin) / float(leftSpan)

    #Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

while True:
    events = inputs.get_gamepad()
    for event in events:
        if event.code == 'ABS_Y':   #Again only interested in
            servoPos = math.floor(translate(event.state, -33000, 33000, 550, 2350)) #convert controller input to safe servo vals
            print(servoPos) #debug puroses
            servoPosb = str(servoPos).encode() #We now have an int but we need an encoded string for .sendto()
            UDPSock.sendto(servoPosb, addr)
            time.sleep(.1)   #sleep to reduce network traffic, trades smoothness for lower trafic
UDPSock.close()
exit()


