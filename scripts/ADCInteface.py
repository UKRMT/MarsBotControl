#!python2.7
#
# ADCInterface.py
#
# Description: 
#   Interface for an ADC object to read data from it. NOTE: currently configured to interface 
#   with a MCP3008 instead of Teensy3.2 current support for the part only has c++ libraries. 
#   
# Revision History:
#   Josh A. 2019-04-12 Initial Version.
#

import os
import time

######## Teensy 3.2 ########
#       
#       SPI
#       CS = P10
#       DOUT = P11
#       DIN = P12
#       SCK = P13
#

######## Connections ########
#   RPi     Teensy 3.2
#   cs   =>   cs
#   MISO <=   DOUT
#   MOSI =>   DIN
#   SCK  <=>  SCK
#   

# PythonIO Libraries, general
import busio
import digitalio
import board

# CircuitPython Libraries for mcp3xxx series ADCs 
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn




class ADCInterface:
    def __init__(self, name, cs="D22", min_in=0, max_in=100):
        self.max = max_in
        self.min = min_in

        # create spi bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        
        # create the chip select
        # when chip select is held high, that ADC will push values to the MISO on the RPi
        cs_pin = getattr(board, cs)
        cs = digitalio.DigitalInOut(cs_pin)

        # create mcp object 
        mcp = MCP.MCP3008(spi,cs)

        # create an analog input channel on pin 
        # the analog signal should be pushed out of P0 on the MCP 
        self.chan = AnalogIn(mcp, MCP.P0)

    ############# public methods #############

    def readADC(self):
        # assuming 12-bit adc -> 2^12 = 4096 per teensy 3.2 spec
        adjusted_value = translateValue(self.chan, 0, 4096, self.min, self.max)
        return adjusted_value

    ############# private methods #############

    def translateValue(self, value, leftMin, leftMax, rightMin, rightMax):
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
        valueScaled = float(value-leftMin)/float(leftSpan)
        return rightMin + (valueScaled * rightSpan)


