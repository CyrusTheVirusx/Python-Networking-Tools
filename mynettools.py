import sys
import socket
import getopt
import threading
import subprocess

# define global variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

# Main function responsible for handling CLI args and calling other functions

def usage():
    print "My Net Tools"
    print
    print "Usage: mynettools.py -t target_host -p port"
    print "-l --listen                 - listen on [host]:[port] for incoming connections"
    print "-e --execute=file_to_run    - execute the given file upon receiving a connection"
    print "-c -command                 - initialize a command shell"
    print "-u --upload=destination     - upon receiving connections upload a file and write to [destination]"
    
    print
    print
    print "Examples: "
    print "mynettools.py -t 192.168.0.1 -p 5555 -l -c"
    print "mynettools.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print "mynettools.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./mynettools.py -t 192.168.0.2 -p 135"
    sys.exit(0)
    
def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    
    if not len(sys.argv[1:]):
        usage()
        
    # read the command line options
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",
                                   ["help","listen","execute","target","port","command","upload"])
    except get.GetoptError as err:
        print str(err)
        usage()
        
    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e","--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False,"Unhandled Option"
            
    # are we going to listen or just send data from stdin?
    
    if not listen and len(target) and port > 0:
        
        # read in the buffer from the command line
        # this will block, so send CTRL-D if not sending input
        # to stdin
        buffer = sys.stdin.read()
        
        #send data off
        client_sender(buffer)
        
    #we are going to listen and upload files and execute commands
    #drop a shell back depending on the CLI options listed
    
    if listen:
        server_loop()
        
        
main()

def client_sender(buffer):
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # connect to the target host
        client.connect((target,port))
        
        if len(buffer):
            client.send(buffer)
            
        while True:
            
            # wait to receive data back
            recv_len = 1
            response = ""
            
            while recv_len:
                
                data = client.recv(4096)
                recv_len = len(data)
                response+= data
                
                if recv_len < 4096:
                    break
                
                print repsonse, 
                
                #wait for more input
                buffer = raw_input("")
                buffer += "\n"
                
                # send buffer
                client.send(buffer)
                
                
    except:
        
        print "[*] Exception! Exiting."
        
        # remove connection
        client.close()
        
def server_loop():
    global target
    