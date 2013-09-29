"""View module

provides View definition where Request object is created and passed
to the function. View function is responsible to provide Response
object.

View are used by defining function which accepts Request object and
additionally URL path arguments and returns Response object. To
register view Router.route decorator is used with URL and HTTP
method as arguments.

"""
import sys

from webob import Request, Response
from webob import exc


def load_view(string):
    """View loader which .

    :param string: must be doted path to ``view_module.view``

    TODO: views should be in app package period.

    """
    module_name, func_name = string.split(':', 1)
    import os
    __import__(module_name)
    module = sys.modules[module_name]
    func = getattr(module, func_name)
    return func


def view(func):
    def replacement(environ, start_response):
        req = Request(environ)
        try:
            resp = func(req, **req.urlvars)
        except exc.HTTPException, e:
            resp = e
        if isinstance(resp, basestring):
            resp = Response(body=resp)
        return resp(environ, start_response)
    return replacement
