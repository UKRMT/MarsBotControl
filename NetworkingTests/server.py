#Wezley Mitchell 9/21/2018
#Simple message receiver listens on a port for incomming UDP messages
import os
from socket import * #Import sockets
host = "" 	     #Leave blank.
port = 5468 	     #Port must be the same as on the client
buf = 1024	     #buffer size in bytes.
addr = (host,port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)
print "Listening..."
while True:
	(data, addr) = UDPSock.recvfrom(buf)
	print "Message: " + data
	if data == "exit":
		break
UDPSock.close()
exit()
