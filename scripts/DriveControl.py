#from roboclaw_3 import RoboClaw
import time
from roboclaw_3 import Roboclaw
import asyncio

# top down view of robot
#
#     (front)
# rc1         rc2
#
#
# M1 []-----[] M3
#      |   |
#      |   |
#      |   |
# M2 []-----[] M4
#
#     (rear)
# M1 -> rc1.m1
# M2 -> rc1.m2
# M3 -> rc2.m1
# M4 -> rc2.m2

class DriveControl:
    def __init__(self):

        self.rc1 = Roboclaw('/dev/roboclaw1', 115200)
        self.rc2 = Roboclaw('/dev/roboclaw2', 115200)

        while self.rc1.Open()==0:
            print('OPEN ROBOCLAW 1 COMMS FAILED, RETRYING...')
            time.sleep(1)
        print('OPENED ROBOCLAW 1 COMMS')

        while self.rc2.Open()==0:
            print('OPEN ROBOCLAW 2 COMMS FAILED, RETRYING...')
            time.sleep(1)
        print('OPENED ROBOCLAW 2 COMMS')

        print('STARTING CURRENT MONITOR LOOP')
        
        #asyncio.ensure_future(self.monitor())
        #asyncio.get_event_loop().run_forever()
        
    def moveLeftSide(self, speed):
        self.drive(self.rc1, 'm1', speed)
        self.drive(self.rc1, 'm2', speed)

    def moveRightSide(self, speed):
        self.drive(self.rc2, 'm1', speed)
        self.drive(self.rc2, 'm2', speed)

    def moveM1(self, speed):
        self.drive(self.rc1, 'm1', speed)

    def moveM2(self, speed):
        self.drive(self.rc1, 'm2', speed)

    def moveM3(self, speed):
        self.drive(self.rc2, 'm1', speed)

    def moveM4(self, speed):
        self.drive(self.rc2, 'm2', speed)

    def drive(self, claw, motor, speed):
        speed = self.ensureValidSpeed(speed)
        direction = 's' # needs to be either f or b to run
        scaledValue = 0;

        if speed <= 1800:
            scaledValue = self.translateValue(speed,1800,0,0,127)
            direction='b'
        elif speed >=2200:
            scaledValue = self.translateValue(speed,2200,4095,0,127)
            direction='f'
        else:
            direction = 'f'
            scaledValue = 0

        # forward and backward go the same direction here becuase the
        # motors are reversed in the wiring
        if motor=='m1':
            if direction=='f':
                claw.ForwardM1(0x80, int(scaledValue))
            elif direction=='b':
                claw.BackwardM1(0x80, int(scaledValue))
            else:
                print('bad direction value')
        elif motor=='m2':
            if direction=='f':
                claw.ForwardM2(0x80, int(scaledValue))
            elif direction=='b':
                claw.BackwardM2(0x80, int(scaledValue))
            else:
                print('bad direction value')
        else:
            print('bad motor index')


    def ensureValidSpeed(self, speed):
        if speed < 0:
            speed = 0
        if speed > 4095:
            speed = 4095
        return speed

    def translateValue(self, value, leftMin, leftMax, rightMin, rightMax):
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
        valueScaled = float(value-leftMin)/float(leftSpan)
        return rightMin + (valueScaled * rightSpan)

#    def monitor(self):
#        cur1 = rc1.ReadCurrents(0x80)
#        cur2 = rc2.ReadCurrents(0x80)
        
