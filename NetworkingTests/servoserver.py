#Wezley Mitchell 9/21/2018
#Takes a number from a udp socket and moves a servo to that position using
#pi gpio
import os
from socket import *
import pigpio
pi = pigpio.pi()
host = ""
port = 5468
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)
print "Waiting for servo command..."
while True:
	(data, addr) = UDPSock.recvfrom(buf)
	if data == "exit":
		break
	servopos = (int)(data)
	if(servopos >= 500 or servopos <= 2500):
		pi.set_servo_pulsewidth(4, servopos)
	elif servopos == 0:
		pi.set_servo_pulsewidth(0, servopos)
UDPSock.close()
exit()
