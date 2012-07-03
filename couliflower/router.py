#!/usr/bin/env python
import re

from webob import Request
from webob import exc

from couliflower.view import load_view, view


var_regex = re.compile(r'''
    \<             # The exact character "{"
    (\w+)          # The variable name (restricted to a-z, 0-9, _)
    (?::([^}]+))?  # The optional :regex part
    \>             # The exact character "}"
    ''', re.VERBOSE)


def build_route(template):
    """URI template matching

    :param template: uri template string
    :returns: regular expression string by template

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
    def __init__(self):
        self.routes = []

    def add_route(self, route, view, **vars):
        if isinstance(view, basestring):
            view = load_view(view)
        route_rule = re.compile(build_route(route))
        self.routes.append((route_rule, view, vars))

    def route(self, route, **vars):
        """Decorator function to register views"""
        def wraper(f):
            self.add_route(route, view(f), **vars)
        return wraper

    def __call__(self, environ, start_response):
        req = Request(environ)
        for regex, controller, vars in self.routes:
            match = regex.match(req.path_info)
            if match:
                req.urlvars = match.groupdict()
                req.urlvars.update(vars)
                return controller(environ, start_response)
        return exc.HTTPNotFound()(environ, start_response)
