import re

from webob import Request
from webob import exc

from cauliflower.view import load_view, view


# this regular expression extracts URI path arguments
var_regex = re.compile(r'''
    \<             # The exact character "{"
    (\w+)          # The variable name (restricted to a-z, 0-9, _)
    (?::([^}]+))?  # The optional :regex part
    \>             # The exact character "}"
    ''', re.VERBOSE)


def build_route(template):
    """Builds regex out of template which then used to match URI path

    :param template: URI path template string which we define in View
    :returns: regular expression string to match URI's

    """
    regex = ''
    last_pos = 0
    for match in var_regex.finditer(template):
        # match all non var delimiters 
        regex += re.escape(template[last_pos:match.start()])
        var_name = match.group(1)
        expr = match.group(2) or '[^/]+'
        expr = '(?P<%s>%s)' % (var_name, expr)
        regex += expr
        last_pos = match.end()
    regex += re.escape(template[last_pos:])
    regex = '^%s$' % regex
    return regex


class Router(object):
    """URI routing to Views

    provides methods and decorators to register URI and attach View.

    Router it self is WSGI application which could run with WSGI
    servers like Python wsgiref.simple_server.

    """

    def __init__(self):
        """Initialise Router instance with empty route list"""
        self.routes = []

    def add_route(self, route, view, **vars):
        """Registers URI route with view and optional args

        :param: route - string containing URI path
        :param: view - view function or string as dotted path to view function
        :param: vars - dict with option URI path arguments

        """
        if isinstance(view, basestring):
            view = load_view(view)
        route_rule = re.compile(build_route(route))
        self.routes.append((route_rule, view, vars))

    def route(self, route, **vars):
        """Decorator for view functions which registers URI to view

        :param: route - string containing URI
        :param: vars - holds URI path arguments
        :returns: wrapper function

        """
        def wraper(f):
            self.add_route(route, view(f), **vars)
        return wraper

    def __call__(self, environ, start_response):
        """WSGI application signature method

        gets called by server passing on environment arguments which
        contains Request information and also information to build
        Response.

        :param: environ - dict holding WSGI environment with request data
        :param: start_response - dict holding WSGI data for response
        :returns: WSGI compatible view function or HTTPNotFound response
                  when View was not found

        """
        request = Request(environ)
        for route_regex, view, vars in self.routes:
            match = route_regex.match(request.path_info)
            if match:
                request.urlvars = match.groupdict()
                request.urlvars.update(vars)
                return view(environ, start_response)
        return exc.HTTPNotFound()(environ, start_response)
