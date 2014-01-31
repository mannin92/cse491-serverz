#!/usr/bin/env python
import random
import socket
import time
import urlparse

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
    fullrequest = conn.recv(1000)
    request=fullrequest.split('\n')[0];
    method = request.split(' ')[0];
    dirtyPath = request.split(' ')[1];
    parse = urlparse.urlparse(dirtyPath);
    path=parse[2];

    #Send a response
    conn.send('HTTP/1.0 200 OK\r\n');
    conn.send('Content-type: text/html\r\n\r\n');
    response_body='';
    if method == 'POST':
        if path == '/submit':
            submit_connection(conn, fullrequest.split('\r\n')[-1]);
    elif method =='GET':
        if path == '/':
            response_body = '<h1>Link to the past</h1>'+ \
                          '<a href = /content>Content</a><br>' + \
                          '<a href = /file>File</a><br>' + \
                          '<a href = /image>Image</a><br>' + \
                          '<a href = /getform>GET Form</a><br>' +\
                          '<a href = /postform>POST Form</a>'
            index_connection(conn, response_body);
        elif path == '/content':
            response_body = '<h1>Khan-tent</h1>Khaannnnnnnnnnn';
            content_connection(conn, response_body);
        elif path == '/file':
            response_body = '<h1>Let\'s go a-filing</h1> :D';
            file_connection(conn, response_body);
        elif path == '/image':
            response_body = '<h1>Gif</h1>Insert cute animal';
            image_connection(conn, response_body);
        elif path =='/getform':
            response_body = "<form action='/submit' method='GET'>\n" + \
                "First name: <input type='text' name='firstname'><br> " + \
                "Last name: <input type='text' name='lastname'>" + \
                "<p><input type='submit' value='Submit'>\n\n" + \
                "</form>"
            form_connection(conn, response_body);    
        elif path =='/postform':
            response_body = "<form action='/submit' method='POST'>\n" + \
                "First name: <input type='text' name='firstname'><br> " + \
                "Last name: <input type='text' name='lastname'>" + \
                "<p><input type='submit' value='Submit'>\n\n" + \
                "</form>"
            form_connection(conn, response_body);    
        elif path == '/submit':
            submit_connection(conn, parse[4]);
		
    conn.close();
    
#this counts as refactoring rightttttt?
def index_connection(conn, input):
	conn.send(input);
	
def content_connection(conn, input):
	conn.send(input);
	
def file_connection(conn, input):
	conn.send(input);
	
def image_connection(conn, input):
	conn.send(input);
    
def form_connection(conn, input):
	conn.send(input);

def submit_connection(conn, input):

#stole this from Cam.
    params = input.split("&")
    
    firstname = params[0].split("=")[1];
    lastname = params[1].split("=")[1];

    conn.send('HTTP/1.0 200 OK\r\n' + \
              'Content-type: text/html\r\n' + \
              '\r\n' + \
              "Hello Mr. %s %s." % (firstname, lastname))
    
    
if __name__ == '__main__':
    main();
