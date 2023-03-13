import cgi
from json import loads, dumps
from urllib import parse as urlparse
from gevent import monkey
from gevent.pywsgi import WSGIServer
from orm import select_all, create_user, select_one_user, update_user, delete_user

monkey.patch_all()


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
    for i, value in enumerate(path):
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
    ret = {
        "status": "",
        "path": path,
        "args": args,
        "method": method,
        "response": "",  # the output of the functions you call
    }
    # GET routes
    # get all users
    if len(path) == 1 and method == "GET":
        start_response("200 OK", [("Content-Type", "application/json")])
        ret["status"] = "200 OK: The request was successful"
        ret["response"] = select_all()
        return [dumps(ret).encode("utf-8")]

    # get one user
    elif len(path) == 2 and method == "GET":
        response = select_one_user(path[1])
        if response == False:
            start_response("404 NOT FOUND", [("Content-Type", "application/json")])
            ret["status"] = "404 Not Found: The requested resource does not exist."
            ret["response"] = "User with uuid: " + path[1] + " does not exist"
        else:
            start_response("200 OK", [("Content-Type", "application/json")])
            ret["status"] = "200 OK: The request was successful"
            ret["response"] = response
        return [dumps(ret).encode("utf-8")]

    # POST routes
    # create a user
    elif len(path) == 1 and method == "POST":
        response = create_user(args)
        if response == "email":
            start_response("409 CONFLICT", [("Content-Type", "application/json")])
            ret[
                "status"
            ] = "409 Conflict: The request conflicts with the current state of the server."
            ret["response"] = "A user with that email address already exists"
        elif response == "phone":
            start_response("409 CONFLICT", [("Content-Type", "application/json")])
            ret[
                "status"
            ] = "409 Conflict: The request conflicts with the current state of the server."
            ret["response"] = "A user with that phone number already exists"
        else:
            start_response("201 CREATED", [("Content-Type", "application/json")])
            ret["status"] = "201 CREATED: The user has been successfully created. "
            ret["response"] = response
        return [dumps(ret).encode("utf-8")]

    # PUT routes
    # update a user
    elif len(path) == 2 and method == "PUT":
        response = update_user(args, path[1])
        if response == "email":
            start_response("409 CONFLICT", [("Content-Type", "application/json")])
            ret[
                "status"
            ] = "409 Conflict: The request conflicts with the current state of the server."
            ret["response"] = "A user with that email address already exists"
        elif response == "phone":
            start_response("409 CONFLICT", [("Content-Type", "application/json")])
            ret[
                "status"
            ] = "409 Conflict: The request conflicts with the current state of the server."
            ret["response"] = "A user with that phone number already exists"
        elif response == False:
            start_response("404 NOT FOUND", [("Content-Type", "application/json")])
            ret["status"] = "404 Not Found: The requested resource does not exist."
            ret["response"] = "User with uuid: " + path[1] + " does not exist"
        else:
            start_response("200 OK", [("Content-Type", "application/json")])
            ret["status"] = "200 OK: The user was successfully updated"
            ret["response"] = response
        return [dumps(ret).encode("utf-8")]

    # DELETE routes
    # delete a user
    elif len(path) == 2 and method == "DELETE":
        response = delete_user(path[1])
        if response == False:
            start_response("404 NOT FOUND", [("Content-Type", "application/json")])
            ret["status"] = "404 Not Found: The requested resource does not exist."
            ret["response"] = "User with uuid: " + path[1] + " does not exist"
        else:
            start_response("200 OK", [("Content-Type", "application/json")])
            ret[
                "status"
            ] = "200 OK: The request was successful and the user has been deleted."
            ret["response"] = response
        return [dumps(ret).encode("utf-8")]

    else:
        ret[
            "response"
        ] = "Make sure that you have /v1.0/users/'userid' after the base URL to access the API. Userid is needed if you want to find one specific user, delete a user, or update them. If you are creating a user or trying to get all users you should just use /v1.0/users/ with the corresponding request method."
        ret[
            "status"
        ] = "400 BAD REQUEST: The request was invalid or could not be understood by the server."
        start_response("400 BAD REQUEST", [("Content-Type", "application/json")])
        return [dumps(ret).encode("utf-8")]


if __name__ == "__main__":
    wsgi_port = 8888
    print("serving on %s..." % wsgi_port)
    WSGIServer(("", wsgi_port), application).serve_forever()
