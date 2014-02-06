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

# Test a / call!
def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Link to the past</h1>'+ \
                      '<a href = /content>Content</a><br>' + \
                      '<a href = /file>File</a><br>' + \
                      '<a href = /image>Image</a><br>' + \
                      '<a href = /getform>GET Form</a><br>' +\
                      '<a href = /postform>POST Form</a>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test a content call
def test_handle_content_connection():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Khan-tent</h1>Khaannnnnnnnnnn'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test a file call
def test_handle_file_connection():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Let\'s go a-filing</h1> :D'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test a image call
def test_handle_image_connection():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Image Page</h1>Insert cute animal'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test a post form
def test_handle_post_form_connection():
    conn = FakeConnection("GET /postform HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' +\
                      "<form action='/submit' method='POST'>\n" +\
                      "First name: <input type='text' name='" +\
                      "firstname'><br> " +\
                      "Last name: <input type='text' name='lastname'>" +\
                      "<p><input type='submit' value='Submit'>\n\n" +\
                      "</form>"

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test a get form
def test_handle_get_form_connection():
    conn = FakeConnection("GET /getform HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' +\
                      "<form action='/submit' method='GET'>\n" +\
                      "First name: <input type='text' name='" +\
                      "firstname'><br> " +\
                      "Last name: <input type='text' name='lastname'>" +\
                      "<p><input type='submit' value='Submit'>\n\n" +\
                      "</form>"

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test a 404 call
def test_handle_four_oh_four_connection():
    conn = FakeConnection("GET /ghfghf HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 404 Not Found\r\n' +\
                      'Content-type: text/html\r\n\r\n' +\
                      '<h1>NOT FOUND</h1>I\'m sorry, but the page you' +\
                      ' have inputted in temporarily not in service. ' +\
                      ' Please try again later.';

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test a (post) 404 call
def test_handle_four_oh_four_connection():
    conn = FakeConnection("POST /ghfghf HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 404 Not Found\r\n' +\
                      'Content-type: text/html\r\n\r\n' +\
                      '<h1>NOT FOUND</h1>I\'m sorry, but the page you' +\
                      ' have inputted in temporarily not in service. ' +\
                      ' Please try again later.';

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test path = /submit
def test_handle_get_submit():
    conn = FakeConnection("GET /submit?firstname=F&" +\
                          "lastname=Darcy HTTP/1.0" + \
                          "HTTP/1.1\r\n\r\n")

    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      "Hello Mr. F Darcy."

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)



# Test path = /submit
def test_handle_post_submit():
    conn = FakeConnection("POST /submit " + \
                          "HTTP/1.1\r\n\r\nfirstname=F&lastname=Darcy")

    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      "Hello Mr. F Darcy."

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

