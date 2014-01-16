#!/usr/bin/env python
import random
import socket
import time

s = socket.socket()         # Create a socket object
host = socket.getfqdn() # Get local machine name
port = random.randint(8000, 9999)
s.bind((host, port))        # Bind to the port

print 'Starting server on', host, port
print 'The Web server URL for this would be http://%s:%d/' % (host, port)

s.listen(5)                 # Now wait for client connection.

print 'Entering infinite loop; hit CTRL-C to exit'
while True:
	# Establish connection with client.    
	c, (client_host, client_port) = s.accept()
	print c.recv(1000)
	#HTTP/1.1 200 OK
	#Content-Type: text/html; charset=utf-8

	print 'Got connection from', client_host, client_port


	response_body_raw = "<html><body><h1>Hello world!</h1>This is xavierdhjr's Web server.</body></html>"
	
	response_headers = {
		'Content-Type': 'text/html; encoding=utf8',
		'Content-Length': len(response_body_raw),
		'Connection': 'close'
	}

	response_headers_raw = ''.join('%s: %s \r\n' % (k, v) for k, v in response_headers.iteritems())
	
	c.send('HTTP/1.1 200 OK \r\n')
        # @comment: Runs fine in chrome, the commented out code should either be accompanied by a 
        # comment explaning the purpose or removed 

#	c.send('Content-Type: text/html; encoding=utf8 \r\n')
#	c.send('Content-Length: %d\r\n' % (len(response_body_raw)))
#	c.send('Connection: close\r\n')
	c.send(response_headers_raw)
	c.send('\r\n') # to separate headers from body
	c.send(response_body_raw)

	c.close()
