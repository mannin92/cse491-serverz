#!/usr/bin/env python
import random
import socket
import time

def main():

    s = socket.socket();         # Create a socket object
    host = socket.getfqdn(); # Get local machine name
    port = random.randint(8000, 9999);
    s.bind((host, port));        # Bind to the port
    
    print 'Starting server on', host, port;
    print 'The Web server URL for this would be http://%s:%d/' % (host, port);
    
    s.listen(5);                 # Now wait for client connection.
    
    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept();
        print 'Got connection from', client_host, client_port;
        handle_connection(c);

def handle_connection(conn):
    
    #Get the request message and parse
    request = conn.recv(1000).split('\n')[0];
    method = request.split(' ')[0];
    path = request.split(' ')[1];

    #Send a response
    conn.send('HTTP/1.0 200 OK\r\n');
    conn.send('Content-type: text/html\r\n\r\n');
    response_body='';
    if method == 'POST':
        response_body = '<h1>GHOST!</h1>Oops, meant \"Post!\"';
    elif path == '/':
        response_body = '<h1>Link to the past</h1>'+ \
                      '<a href = /content>Content</a><br>' + \
                      '<a href = /file>File</a><br>' + \
                      '<a href = /image>Image</a>'
    elif path == '/content':
        response_body = '<h1>Khan-tent</h1>Khaannnnnnnnnnn';
    elif path == '/file':
        response_body = '<h1>Let\'s go a-filing</h1> :D';
    elif path == '/image':
        response_body = '<h1>Gif</h1>Insert cute animal';

    conn.send(response_body);
    conn.close();


if __name__ == '__main__':
    main();
