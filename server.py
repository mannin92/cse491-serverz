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

    #need to change thissssss
    fullrequest = conn.recv(1000)
    request=fullrequest.split('\n')[0].split(' ');

    method = request[0];
    dirtyPath = request[1];

    try:
        parse = urlparse.urlparse(dirtyPath);
        path=parse[2];

    except:
       path = "/404"
       four_oh_four_connection(conn, ' ');

    if method == 'POST':
        if path == '/submit':
            #parameters are at end of request, get last item
            #in this case, param is user name
            submit_connection(conn, fullrequest.split('\r\n')[-1]);
        else:
            four_oh_four_connection(conn, ' ');
    elif method =='GET':
        if path == '/':
            index_connection(conn, ' ');
        elif path == '/content':
            content_connection(conn, ' ');
        elif path == '/file':
            file_connection(conn, ' ');
        elif path == '/image':
            image_connection(conn, ' ');
        elif path =='/getform':
            form_get_connection(conn, ' ');    
        elif path =='/postform':
            form_post_connection(conn, ' ');  
        elif path == '/submit':
            #in the case of get, the param are in the url
            submit_connection(conn, parse[4]);
        else:
           four_oh_four_connection(conn, ' ');
		
    conn.close();
    
#just to be used when not 404, kinda redundant.
def good_connection(conn):
    #Send a response
    conn.send('HTTP/1.0 200 OK\r\n');
    conn.send('Content-type: text/html\r\n\r\n');


#param is currently a blank parameter to be added later
def index_connection(conn, param):
    response_body = '<h1>Link to the past</h1>'+ \
                    '<a href = /content>Content</a><br>' + \
                    '<a href = /file>File</a><br>' + \
                    '<a href = /image>Image</a><br>' + \
                    '<a href = /getform>GET Form</a><br>' +\
                    '<a href = /postform>POST Form</a>'
    good_connection(conn);
    conn.send(response_body);
	
def content_connection(conn, param):
    response_body = '<h1>Khan-tent</h1>Khaannnnnnnnnnn';
    good_connection(conn);
    conn.send(response_body);
	
def file_connection(conn, param):
    response_body = '<h1>Let\'s go a-filing</h1> :D';
    good_connection(conn);
    conn.send(response_body);
	
def image_connection(conn, param):
    response_body = '<h1>Gif</h1>Insert cute animal';
    good_connection(conn);
    conn.send(response_body);
    
def form_post_connection(conn, param):
    response_body = "<form action='/submit' method='POST'>\n" + \
                "First name: <input type='text' name='firstname'><br> " + \
                "Last name: <input type='text' name='lastname'>" + \
                "<p><input type='submit' value='Submit'>\n\n" + \
                "</form>"
    good_connection(conn);
    conn.send(response_body);

def form_get_connection(conn, param):
    response_body = "<form action='/submit' method='GET'>\n" + \
                "First name: <input type='text' name='firstname'><br> " + \
                "Last name: <input type='text' name='lastname'>" + \
                "<p><input type='submit' value='Submit'>\n\n" + \
                "</form>"
    good_connection(conn);
    conn.send(response_body);

#def unknown_connection(conn, param):
#    response_body = '<h1>???</h1>How did we get here?';
#    conn.send(response_body);

def four_oh_four_connection(conn, param):
    conn.send('HTTP/1.0 404 Not Found\r\n');
    conn.send('Content-type: text/html\r\n\r\n');
    response_body = '<h1>NOT FOUND</h1>I\'m sorry, but the page you' +\
                    ' have inputted in temporarily not in service. ' +\
                    ' Please try again later.';
    conn.send(response_body);

#submit path is handled, should be called when form submitted
def submit_connection(conn, param):

    #magggiiicc
    param = urlparse.parse_qs(param)
    
    # pull out the info we want
    firstname = param['firstname'][0]
    lastname  = param['lastname'][0]

    conn.send('HTTP/1.0 200 OK\r\n' + \
              'Content-type: text/html\r\n' + \
              '\r\n' + \
              "Hello Mr. %s %s." % (firstname, lastname))
    
    
if __name__ == '__main__':
    main();
