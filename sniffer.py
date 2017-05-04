import os
import socket

host = "192.168.0.8"

if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP
    
sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

sniffer.bind((host,0))

#IP included in capture

sniffer.setscokopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

#set up promiscuous mode
if os.name == "nt":
	sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
	
#read in a single packet
print sniffer.recvfrom(65565)

#Turn off promiscuous mode
if os.name == "nt":
	sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

