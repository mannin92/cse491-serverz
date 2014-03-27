#!/usr/bin/env python
import random
import socket
import time
import urlparse
import cgi

from StringIO import StringIO
from app import make_app
from sys import stderr
from wsgiref.validate import validator

def main(socketmodule=None):
    if socketmodule is None:
        socketmodule = socket
    
    s = socket.socket();  # Create a socket object
    host = socket.getfqdn(); # Get local machine name

    argParser = argparse.ArgumentParser(description='Set up WSGI server')
    argParser.add_argument('-A', metavar='App', type=str,
                            default=['myapp'],
                            choices=['myapp', 'imageapp', 'altdemo'],
                            help='Select which app to run', dest='app')
    argParser.add_argument('-p', metavar='Port', type=int,
                            default=-1, help='Select a port to run on',
                            dest='p')
    argVals = argParser.parse_args()

    app = argVals.app
    if app == 'altdemo': 
        ## Quixote altdemo
        import quixote
        from quixote.demo.altdemo import create_publisher
        p = create_publisher()
        wsgi_app = quixote.get_wsgi_app()
        ##

    elif app == 'imageapp':
        ## Image app
        import quixote
        import imageapp
        from imageapp import create_publisher
        p = create_publisher()
        imageapp.setup()
        wsgi_app = quixote.get_wsgi_app()
        ##

    else:
        ## My app.py
        from app import make_app
        wsgi_app = make_app()
        ## 

    # Bind to a (random) port
    port = argVals.p if argVals.p != -1 else random.randint(8000,9999)
    s.bind((host, port))


    print 'Starting server on', host, port;
    print 'The Web server URL for this would be http://%s:%d/' % (host, port);
    
    s.listen(5);  # Now wait for client connection.
    
    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept();
        print 'Got connection from', client_host, client_port;
        handle_connection(c, client_port);


def handle_connection(conn, port):
    environ = {}
    request = conn.recv(1)
  
    if not request:
        print 'Error, client closed'
        return
    
    # This will get all the headers
    while request[-4:] != '\r\n\r\n':
        request += conn.recv(1)

    request, data = request.split('\r\n',1)
    headers = {}
    for line in data.split('\r\n')[:-2]:
        k, v = line.split(': ', 1)
        headers[k.lower()] = v

    path = urlparse(request.split(' ', 3)[1])
    
    environ['REQUEST_METHOD'] = 'GET'
    environ['PATH_INFO'] = path[2]
    environ['QUERY_STRING'] = path[4]
    environ['CONTENT_TYPE'] = 'text/html'
    environ['CONTENT_LENGTH'] = str(0)
    environ['SCRIPT_NAME'] = ''
    environ['SERVER_NAME'] = socket.getfqdn()
    environ['SERVER_PORT'] = str(port)
    environ['wsgi.version'] = (1, 0)
    environ['wsgi.errors'] = stderr
    environ['wsgi.multithread']  = False
    environ['wsgi.multiprocess'] = False
    environ['wsgi.run_once']     = False
    environ['wsgi.url_scheme'] = 'http'
    environ['HTTP_COOKIE'] = headers['cookie'] if 'cookie' in headers.keys() else ''

    body = ''
    if request.startswith('POST '):
        environ['REQUEST_METHOD'] = 'POST'
        environ['CONTENT_LENGTH'] = headers['content-length']
        environ['CONTENT_TYPE'] = headers['content-type']
        while len(body) < int(headers['content-length']):
            body += conn.recv(1)

    def start_response(status, response_headers):  
        conn.send('HTTP/1.0 ')
        conn.send(status)
        conn.send('\r\n')
        for pair in response_headers:
            key, header = pair
            conn.send(key + ': ' + header + '\r\n')
        conn.send('\r\n')
		
		
    environ['wsgi.input'] = StringIO(body)
    my_app = make_app()
    validator_app = validator(my_app)
    result = my_app(environ, start_response)
    for data in result:
        conn.send(data)
    conn.close()
		
  
  
if __name__ == '__main__':
    main();
