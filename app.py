# from http://docs.python.org/2/library/wsgiref.html
import cgi
import urlparse
import jinja2
from wsgiref.util import setup_testing_defaults

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def simple_app(environ, start_response):
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)

    print(environ)

    # By default, set up the 404 page response. If it's
    # a valid page, we change this. If some weird stuff
    # happens, it'll default to 404.
    status = '404 Not Found'
    response_content = not_found('', env)
    headers = [('Content-type', 'text/html')]
    
    try:
        http_method = environ['REQUEST_METHOD']
        path = environ['PATH_INFO']
    except:
        pass

    if http_method == 'POST':
        if path == '/':
            status = '200 OK'
            response_content = handle_index(environ, env)
        elif path == '/submit':
            status = '200 OK'
            response_content = handle_submit_post(environ, env)
    elif http_method == 'GET':
        if path == '/':
            status = '200 OK'
            response_content = handle_index(environ, env)
        elif path == '/content':
            status = '200 OK'
            response_content = handle_content(environ, env)
        elif path == '/file':
            status = '200 OK'
            response_content = handle_file(environ, env)
        elif path == '/image':
            status = '200 OK'
            response_content = handle_image(environ, env)
        elif path == '/submit':
            status = '200 OK'
            response_content = handle_submit_get(environ, env)
                
    start_response(status, headers)
    return response_content

def make_app():
    return simple_app

def handle_index(params, env):
    return str(env.get_template("index.html").render())
    
def handle_content(params, env):
    return str(env.get_template("content.html").render())

def handle_file(params, env):
    return str(env.get_template("file.html").render())

def handle_image(params, env):
    return str(env.get_template("image.html").render())

def not_found(params, env):
    return str(env.get_template("404.html").render())

def handle_submit_post(environ, env):
    ''' Handle a connection given path /submit '''
    # submit needs to know about the query field, so more
    # work needs to be done here.

    # we want the first element of the returned list
    headers = {}
    for k in environ.keys():
        headers[k.lower()] = environ[k]

    form = cgi.FieldStorage(headers = headers, fp = environ['wsgi.input'], 
                            environ = environ)

    try:
      firstname = form['firstname'].value
    except KeyError:
      firstname = ''
    try:
      lastname = form['lastname'].value
    except KeyError:
      lastname = ''

    print form
    vars = dict(firstname = firstname, lastname = lastname)
    return str(env.get_template("submit.html").render(vars))

def handle_submit_get(environ, env):

    # we want the first element of the returned list
    params = environ['QUERY_STRING']
    params = urlparse.parse_qs(params)

    try:
      firstname = params['firstname'][0]
    except KeyError:
      firstname = ''
    try:
      lastname = params['lastname'][0]
    except KeyError:
      lastname = ''

    vars = dict(firstname = firstname, lastname = lastname)
    return str(env.get_template("submit.html").render(vars))