import cgi, types
from json import loads, dumps
from copy import deepcopy
from urllib import parse as urlparse
from gevent import monkey

monkey.patch_all()
from gevent.pywsgi import WSGIServer
import gevent
from orm import select_all, create_user, select_one_user, update_user, delete_user


# what did the types get updated to for python3
def parseAndDelistArguments(args):
    print("Line 11: ", type(args))
    # checking if type of args is string or unicode, and that the first character is a curly brace or square bracket
    if type(args) == str and args[:1] in ["{", "["]:
        args = loads(args)
        if type(args) == list:
            return args
    else:
        args = urlparse.parse_qs(args)

    return delistArguments(args)


def delistArguments(args):
    """
    Takes a dictionary, 'args' and de-lists any single-item lists then
    returns the resulting dictionary.
    {'foo': ['bar']} would become {'foo': 'bar'}
    """

    def flatten(k, v):
        if len(v) == 1 and type(v) is list:
            return (str(k), v[0])
        return (str(k), v)

    return dict([flatten(k, v) for k, v in args.items()])


def application(env, start_response):
    path = env["PATH_INFO"]
    print("_wsgi.path(initial):", path)

    if path == "/":
        start_response("302 Moved Temporarily", [("Location", "http://blueboard.com")])
        return ""

    if path == "/favicon.ico":
        start_response(
            "301 Moved Permanently", [("Location", "http://blueboard.com/favicon.ico")]
        )
        return ""

    path = path.split("/")
    for (i, value) in enumerate(path):
        path[i] = value.strip()

    if len(path) < 2 or path[1] != "v1.0":
        start_response("500 Internal Server Error", [("Content-Type", "text/plain")])
        return ["invalid API version, try v1.0".encode("utf-8")]

    path = path[2:]
    if not path[-1]:
        path.pop()
    print("_wsgi.path(cleaned):", path)

    method = env["REQUEST_METHOD"].upper()
    print("method:", method)

    print(env["QUERY_STRING"])
    args = parseAndDelistArguments(env["QUERY_STRING"])
    print("args: 63 ", args)

    # env variable, check it out in docs
    wsgi_input = env["wsgi.input"]
    # print(wsgi_input.read())

# I removed the "and method != "POST" from the below condition, because if it is a post the "args" are in byte type. If this causes errors later on look back to this edit.
    if wsgi_input.content_length:
        post_env = env.copy()
        post_env["QUERY_STRING"] = ""
        form = cgi.FieldStorage(
            fp=env["wsgi.input"], environ=post_env, keep_blank_values=True
        )
        # list comprehension: A for loop that outputs a list. Takes in data and makes a list out of it. Added ".strip()" to the values to get rid of whitespace
        form_data = [(k.strip(), form[k].value.strip()) for k in form.keys()]
        # turns list into dictionary
        args.update(form_data)

    if method == "PUT":
        wsgi_input = wsgi_input.read()
        args.update(parseAndDelistArguments(wsgi_input))
        print("ARGS", args)

    # now call the methods as needed
	# ROUTES

    if "users" in path and len(path) <= 2:
        # GET routes
        if len(path) == 1 and method == "GET":
            start_response("200 OK", [("Content-Type", "text/html")])
            response = select_all()

            
        if len(path) == 2 and method == "GET":
            start_response("200 OK", [("Content-Type", "text/html")])
            response = select_one_user(path[1])

        # POST routes
        if method == "POST":
            start_response("200 OK", [("Content-Type", "text/html")])
            response = create_user(args)
            
        # PUT routes
        if len(path) == 2 and method == "PUT":
            start_response("200 OK", [("Content-Type", "text/html")])
            response = update_user(args, path[1])
 
        # DELETE routes
        if len(path) == 2 and method == "DELETE":
            start_response("200 OK", [("Content-Type", "text/html")])
            response = delete_user(path[1])

        ret = {
            "path": path,
            "args": args,
            "method": method,
            "response": response,  # the output of the functions you call
        }
        start_response("200 OK", [("Content-Type", "application/json")])
        return [dumps(ret).encode("utf-8")]
    else:
        response = "make sure that you have /v1.0/users/'userid' after the base URL to access the API, userid is needed if you want to find one specific user, delete a user, or update them."
        ret = {
            "path": path,
            "args": args,
            "method": method,
            "response": response,  # the output of the functions you call
        }
        start_response("500 Internal Server Error", [("Content-Type", "application/json")])
        return [dumps(ret).encode("utf-8")]



if __name__ == "__main__":
    wsgi_port = 8888
    print("serving on %s..." % wsgi_port)
    WSGIServer(("", wsgi_port), application).serve_forever()
