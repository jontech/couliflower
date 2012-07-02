#!/usr/bin/env python
import sys

from webob import Request, Response
from webob import exc


def load_view(string):
    """Loads view from specific module.

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
