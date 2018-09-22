#Wezley Mitchell 9/21/2018
#Simple Message Sender using UDP sockets
import os
from socket import *	#Import sockets
host = "192.168.1.13"	#IP of the listener.
port = 5468		#Port to send on
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
while True:
	data = raw_input("Enter message (to end type 'exit'): ")
	UDPSock.sendto(data, addr)
	if data == "exit":
		break
UDPSock.close()
exit()
