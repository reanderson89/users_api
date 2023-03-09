import cgi, types
from json import loads, dumps
from copy import deepcopy
from urllib import parse as urlparse
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
import gevent

# what did the types get updated to for python3
def parseAndDelistArguments(args):
	print("Line 11: ",type(args))
	# checking if type of args is string or unicode, and that the first character is a curly brace or square bracket
	if type(args) == str and args[:1] in ['{', '[']:
		args = loads(args)
		if type(args) == list: return args;
	else:
		args = urlparse.parse_qs(args)

	return delistArguments(args)


def delistArguments(args):
	'''
		Takes a dictionary, 'args' and de-lists any single-item lists then
		returns the resulting dictionary.
		{'foo': ['bar']} would become {'foo': 'bar'}
	'''
	
	def flatten(k,v):
		if len(v) == 1 and type(v) is list: return (str(k), v[0]);
		return (str(k), v)

	return dict([flatten(k,v) for k,v in args.items()])


def application(env, start_response):
	path = env['PATH_INFO']
	print('_wsgi.path(initial):', path)

	if path == '/':
		start_response('302 Moved Temporarily', [('Location', 'http://blueboard.com')])
		return ''

	if path == '/favicon.ico': 
		start_response('301 Moved Permanently', [('Location', 'http://blueboard.com/favicon.ico')])
		return ''
	
	path = path.split('/')
	if len(path) < 2 or path[1] != 'v1.0':
		start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
		return 'invalid API version'

	path = path[2:]
	if not path[-1]: path.pop();
	print('_wsgi.path(cleaned):', path)

	method = env['REQUEST_METHOD'].upper()
	print('method:', method)
	
	print(env['QUERY_STRING'])
	args = parseAndDelistArguments(env['QUERY_STRING'])
	print('args: 63 ', args)

# env variable, check it out in docs
	wsgi_input = env['wsgi.input']

	if wsgi_input.content_length and method != 'PUT':
		post_env = env.copy()
		post_env['QUERY_STRING'] = ''
		form = cgi.FieldStorage(
			fp=env['wsgi.input'],
			environ=post_env,
			keep_blank_values=True
		)
		# list comprehension: pythonic thing, a for statement that outputs a list. Takes in data and makes a list out of it.
		form_data = [(k, form[k].value) for k in form.keys()]
		# what does "update" do to a dictionary?
		args.update(form_data)

	if method == 'PUT':	
		wsgi_input = wsgi_input.read()
		args.update(parseAndDelistArguments(wsgi_input))

	#now call the methods as needed
	# test
	
	if "users" in path:
		start_response('200 OK', [('Content-Type', 'text/html')])
		response = "Hello World"


	try:
		ret = { 
			'path' : path,
			'args' : args,
			'method' : method,
			'response': response #the output of the functions you call
		}
		start_response('200 OK', [('Content-Type', 'application/json')])
		print(dumps(ret).encode("utf-8"))
		return [dumps(ret).encode("utf-8")]

	except Exception as inst:
		print("line: 106", inst)
		start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
		return repr(inst)


if __name__ == '__main__':
	wsgi_port = 8888
	print('serving on %s...' % wsgi_port)
	WSGIServer(('', wsgi_port), application).serve_forever()
