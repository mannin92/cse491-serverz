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
    print 'Got connection from', client_host, client_port
    c.send('HTTP/1.0 200 OK\r\n') 
    
    # alternative way
    # s.send('%s %s %s' % (response_proto, response_status, response_status_text))

    # header details
    c.send('Content-Type: text/html\r\n\r\n')

    response_body = "<h1>Hello, world!</h1> This is mannin92's web server\r\n"
    c.send(response_body)
    c.close()
