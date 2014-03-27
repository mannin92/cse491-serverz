#! /usr/bin/env python
import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False
		self.n_times_accept_called = 0

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

    def bind(self, param):
        (host, port) = param

    def listen(self, n):
        assert n ==5
        if n !=5
            raise Exception("wrong n")

class FakeSocketModule(object):    
    def getfqdn(self):        
        return "fakehost"    

    def socket(self):        
        return FakeConnection("")
		
class AcceptCalledMultipleTimes(Exception):
    pass	
	
	

# Test a basic GET call.
def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")

    server.handle_connection(conn, 80)

    assert 'HTTP/1.0 200' in conn.sent and 'form' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# Test path = /content
def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")

    server.handle_connection(conn, 80)
	result = conn.sent

    assert 'HTTP/1.0 200' in conn.sent and 'content' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# Test path = /file
def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")

    server.handle_connection(conn, 80)

    assert 'HTTP/1.0 200' in conn.sent and 'File' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# Test path = /content
def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>All kinds of content</h1>' + \
                      'Khannnn.'

    server.handle_connection(conn, 80)
    print conn.sent
    assert 'HTTP/1.0 200' in conn.sent and 'image' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# Test path = /submit
def test_handle_submit():
    conn = FakeConnection("GET /submit?firstname=Fitzwilliam&lastname=Darcy" + \
                          " HTTP/1.1\r\n\r\n")

    server.handle_connection(conn, 80)

    assert 'html' in conn.sent and "Fitzwilliam" in conn.sent \
      and 'Darcy' in conn.sent, 'Got: %s' % (repr(conn.sent),)

# Test a submit with no first name
def test_handle_submit_no_first_name():
    conn = FakeConnection("GET /submit?firstname=&lastname=Darcy" + \
                          " HTTP/1.1\r\n\r\n")

    server.handle_connection(conn, 80)

    assert 'html' in conn.sent and "Darcy" in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# Tests a submit with no last name
def test_handle_submit_no_last_name():
    conn = FakeConnection("GET /submit?firstname=Fitzwilliam&lastname=" + \
                          " HTTP/1.1\r\n\r\n")

    server.handle_connection(conn, 80)

    assert 'html' in conn.sent and "Fitzwilliam" in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# test 404
def test_handle_not_found():
    conn = FakeConnection("GET /bad HTTP/1.0\r\n\r\n")

    server.handle_connection(conn, 80)
    assert 'HTTP/1.0 404' in conn.sent and 'service' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# Test POST connections

# Test / requests
def test_handle_connection_post():
    conn = FakeConnection("POST / HTTP/1.0\r\n" + \
      "Content-length: 0\r\n\r\n")

    server.handle_connection(conn, 80)
    assert 'HTTP/1.0 200' in conn.sent and 'form' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# Test /submit requests (both types)
def test_handle_submit_post():
    conn = FakeConnection("POST /submit HTTP/1.1\r\n" + \
                          "Content-Length: 31\r\n\r\n" + \
                          "firstname=Fitzwilliam&lastname=Darcy")

    server.handle_connection(conn, 80)
    
    assert 'HTTP/1.0 200' in conn.sent and "Hello Mrs." in conn.sent, \
    'Got: %s' % (repr(conn.sent),)
    
def test_handle_submit_post_multipart_and_form_data():
    conn = FakeConnection("POST /submit " + \
          "HTTP/1.1\r\nContent-length: 246\r\n\r\n------" + \
          "WebKitFormBoundaryAaal27xQakxMcNYm\r\n" + \
          'Content-Disposition: form-data; name="firstname"\r\n\r\nFitzwilliam' + \
          '\r\n------WebKitFormBoundaryAaal27xQakxMcNYm\r\n' + \
          'Content-Disposition: form-data; name="lastname"\r\n\r\nDarcy' + \
          '\r\n------WebKitFormBoundaryAaal27xQakxMcNYm--")')

    server.handle_connection(conn, 80)
    
    assert 'HTTP/1.0 200' in conn.sent and "Hello Mrs." in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# test 404
def test_handle_not_found_post():
    conn = FakeConnection("POST /notOkay HTTP/1.1\r\n" + \
                          "Content-Length: 31\r\n\r\n" + \
                          "firstname=Fitzwilliam&lastname=Darcy")

    server.handle_connection(conn, 80)
    assert 'HTTP/1.0 404' in conn.sent and 'temporarily' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# Handle large request
def test_handle_long_request():
    firstname = lastname = "asdfasdfasdfasdfasdf" * 100
    conn = FakeConnection("POST /submit HTTP/1.1\r\n" + \
                          "Content-Length: 4020\r\n\r\n" + \
                          "firstname=%s&lastname=%s" % (firstname, lastname))

    server.handle_connection(conn, 80)
    
    assert 'HTTP/1.0 200' in conn.sent and "Hello Mrs." in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# Test an empty request
def test_handle_empty_request():
  conn = FakeConnection("\r\n\r\n")

  server.handle_connection(conn, 80)

  assert 'HTTP/1.0 404' in conn.sent and 'try again' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)
	
def test_main():
    fakemodule = FakeSocketModule()

    success = False
    try:
        server.main(fakemodule)
    except AcceptCalledMultipleTimes:
        success = True
        pass

    assert success, "Something went wrong"

