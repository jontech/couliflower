#!/usr/bin/env python
import re

from webob import Request
from webob import exc

from couliflower.helpers import load_view


var_regex = re.compile(r'''
    \<             # The exact character "{"
    (\w+)          # The variable name (restricted to a-z, 0-9, _)
    (?::([^}]+))?  # The optional :regex part
    \>             # The exact character "}"
    ''', re.VERBOSE)


def build_regex(template):
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

    def add_route(self, template, controller, **vars):
        if isinstance(controller, basestring):
            controller = load_view(controller)
        self.routes.append((re.compile(build_regex(template)),
                            controller,
                            vars))

    def __call__(self, environ, start_response):
        req = Request(environ)
        for regex, controller, vars in self.routes:
            match = regex.match(req.path_info)
            if match:
                req.urlvars = match.groupdict()
                req.urlvars.update(vars)
                return controller(environ, start_response)
        return exc.HTTPNotFound()(environ, start_response)
