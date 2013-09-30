import re

from webob import Request
from webob import exc


# this regular expression extracts URI path arguments
var_regex = re.compile(r'''
    \<             # The exact character "{"
    (\w+)          # The variable name (restricted to a-z, 0-9, _)
    (?::([^}]+))?  # The optional :regex part
    \>             # The exact character "}"
    ''', re.VERBOSE)


def build_route(template):
    """Builds regex out of path defined creating View

    :param template: URI path string which we define in View
    :returns: regular expression string to match URIs

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
    """URI routing throughout View functions

    provides methods and decorators to register URI to a function

    Router it self is WSGI application which could run with WSGI
    servers like wsgiref.

    """

    def __init__(self):
        """Initialise Router instance with empty route list"""
        self.routes = []

    def add_route(self, route, view):
        """Registers URI route with view

        :param: route - string containing URI path
        :param: view - callable view function

        """
        route_rule = re.compile(build_route(route))
        self.routes.append((route_rule, view))

    def route(self, route):
        """Decorates View function which is then gets registered

        :param: route - string containing URI path
        :returns: View register function

        """
        def wrapper(view):
            """Registers URI path regex to a view"""
            self.add_route(route, view)
        return wrapper

    def __call__(self, environ, start_response):
        """WSGI application signature method

        gets called by server passing on environment arguments which
        contains Request information and also information to build
        Response.

        This is the place where Response object gets built and Response
        from View is called to start actual response.

        :param: environ - dict holding WSGI environment with request data
        :param: start_response - dict holding WSGI data for response
        :returns: WSGI compatible view function or HTTPNotFound response
                  when View was not found

        """
        request = Request(environ)
        for route_regex, view in self.routes:
            match = route_regex.match(request.path_info)
            if match:
                uri_args = match.groupdict()
                resp = view(request, **uri_args)
                return resp(environ, start_response)
        return exc.HTTPNotFound()(environ, start_response)
