# Python-Networking-Tools

-------------------------

#TCP_CLIENT
----------

Basic TCP Client to send and recieve data

(The server is always expecting us to send data first)


#UDP_CLIENT
----------

SOCK_DRGRAM = UDP identifier

sendto() = pass in the data and the server you wish to send data to

recvfrom() = to retrieve a response frm the server (returns data and details of the remote host and port)

#TCP_SERVER
----------

Pass in the IP and port we want the server to listen on

Tell the server to start listening

with a max backlog of connections set to 5

Server enters its main loop where it waits for an incoming connection

when the client connects, we receive the client socket and place it in the client variable. and the remote connection details to the addr variable

#MY_NET_TOOLS
-------------

network client and server to push data 

listener to get cli access


