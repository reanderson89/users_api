from gevent.pywsgi import WSGIServer
from json import loads, dumps

def application(env, start_response):
    if env['PATH_INFO'] == '/':
        start_response('200 OK', [('Content-Type','text/html')])
        return [b"<b>Hello World</b>"]

    if env['PATH_INFO'] == '/users':
        start_response('200 OK', [('Content-Type','text/html')])
        return [b"<h1>List of users</h1>"]
    start_response('404 Not Found', [('Content-Type','text/html')])
    return [b"<h1>Not Found</h1>"]

print(f"Serving on port 8080")
WSGIServer(('127.0.0.1',8080), application).serve_forever()