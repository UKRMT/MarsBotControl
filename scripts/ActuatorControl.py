#!python2.7
#
# ActuatorControl.py
#
# Description: 
#   Code for controlling the arm actuators. It verifies a valid speed and position using 
#   ADCInterface, and then moves the arm using roboclaw. NOTE: This code assumes that a 
#   webosocket connection will be continuously sending move requests and therefore the 
#   position checks happen in move. If signal is lost while the actuator is moving it 
#   could overdrive the motor since there are no checks. Solution would be to create interrupt 
#   driven position handler
#

#   
# Revision History:
#   Josh A. 2019-04-12 Initial Version.
#

import time
from roboclaw_3 import Roboclaw
import ADCInterface as Actuator


class ActuatorControl:
    # max and min values that the ADCInterface will send
    MAX_POS = 100
    MIN_POS = 0
    def __init__(self):
        self.act =  Roboclaw('/dev/roboclaw3', 115200)
        while self.act.Open()==0:
            print("Failed to open actuator comms, trying again.")
            time.sleep(1)
        print("Opened Actuator roboclaw")

    ############# public methods #############

    # set adc interface for reading the current position of the actuator
    def setInterface(self, adcObj):
        #expects an adc interface object
        self.act_interface =  adcObj
        self.pos = self.act_interface.readADC()

    #  move up with the option of specifying speed
    def moveUp(self, speed=False):
        #refresh position
        self.pos = self.act_interface.readADC()
        if not speed:
            self.moveActBinary(1799)
        else: 
            self.moveActScalar(speed)

    # move down with the option of specifying speed
    def moveDown(self, speed=False):
        #refresh position
        self.pos = self.act_interface.readADC()
        if not speed:
            self.moveActBinary(2201)
        else: 
            self.moveActScalar(speed)
    def stop(self):
        self.moveActBinary(2000)
    



    ############# private methods #############

    # single speed actuator movement
    def moveActBinary(self, speed):
        speed = verify_speed(speed)
        if speed <= 1800:
            self.act.ForwardM1(0x80, -50)
        elif speed <= 2200:
            self.act.BackwardM1(0x80, 50)
        else:
            self.act.ForwardM1(0x80, 0)
    
    # variable speed actuator movement
    def moveActScalar(self, speed):
        speed = self.verify_speed(speed)
        if speed <= 1800:
            # move actuator forward
            adjusted_speed = translate_value(speed, 1800,0,0,127)
            direction = "b"
        elif speed >= 2200:
            #move actuator backward
            adjusted_speed = translate_value(speed, 2200, 4095,0,127)
            direction = "f"
        else : 
            #do not move actuator
            direction = "s"
            adjusted_speed = 0

        if direction == "f" : 
            self.act.ForwardM1(0x80, adjusted_speed)
        elif direction == "b":
            self.act.BackwardM1(0x80, adjusted_speed)
        else: 
            self.act.ForwardM1(0x80, 0)

    # verifies speed and position 
    def verify_speed(self, speed):
        # set maximum speed that the actuator can go 
        maximum = 4095

        # cap the speed at the max in either direction
        if speed > maximum:
            speed = maximum
        elif speed < 0:
            speed = 0
        else: 
            speed = speed
        
        # make sure not to drive the actuators with no more left
        if self.pos >= MAX_POS and speed > 2000:
            speed = 2000
        elif self.pos <= MIN_POS and speed < 2000:
            speed = 2000
        else:
            speed = speed

        return speed

    # translates vale from left range to right range
    def translate_value(self, value, leftMin, leftMax, rightMin, rightMax):
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
        valueScaled = float(value-leftMin)/float(leftSpan)
        return rightMin + (valueScaled * rightSpan)
        
