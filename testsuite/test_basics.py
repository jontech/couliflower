# -*- coding: utf-8 -*-
import types
from unittest import TestCase, TestLoader

from webob import Request

from cauliflower.router import build_route, Router
from cauliflower.view import load_view, view


def iscallable(thing):
    """Tests if argument is a function"""
    return isinstance(thing, types.FunctionType)


class TestHelpers(TestCase):
    """Check helper functions output"""

    def test_load_view(self):
        """Should load view function by string representation"""
        view = load_view('test_views:dobla')
        # FIXME: how about class-based views??
        self.assertTrue(iscallable(view))


class TestRegexPaths(TestCase):
    """Test URI template to regex mapping"""

    def test_static_path(self):
        """Should create regex to match URI path without args"""
        res = build_route('/a/static/path')
        self.assertEqual(res, '^\/a\/static\/path$')

    def test_arg_in_path(self):
        """Should make re to match args in URI path"""
        res = build_route('/<foo>')
        self.assertEqual(res, '^\\/(?P<foo>[^/]+)$')

    def test_arg_validation(self):
        """Should verify path argument as string length 16"""
        # TODO: not implemented
        pat = '/<string:foo[16]>'
        pass


class TestRouting(TestCase):
    """Test the routing from URI to view loaded"""

    def setUp(self):
        self.router = Router()

    def tearDown(self):
        del self.router

    def test_index_uri(self):
        """Should register root URI path using router"""
        def dofoo():
            return 'yay'
        self.router.add_route('/', dofoo)
        self.assertEqual(len(self.router.routes), 1)
        res_repath, res_view, res_extra = self.router.routes[0]
        self.assertEqual(res_repath.pattern, '^\/$')
        self.assertEqual(res_view, dofoo)
        self.assertEqual(res_extra, {})

    def test_decorated_view(self):
        """Should register root URI path using router decorator"""
        @self.router.route('/')
        def dofoo():
            return 'yay'
        self.assertEqual(len(self.router.routes), 1)
        res_repath, res_view, res_extra = self.router.routes[0]
        self.assertEqual(res_repath.pattern, '^\/$')
        self.assertTrue(iscallable(res_view))
        self.assertEqual(res_extra, {})

    def test_pathargs_rule(self):
        """Should register regex to parse args from URI path"""
        def dofoo():
            return 'yay'
        self.router.add_route('/<foo>', dofoo)
        self.assertEqual(len(self.router.routes), 1)
        res_repath, res_view, res_extra = self.router.routes[0]
        self.assertEqual(res_repath.pattern, '^\\/(?P<foo>[^/]+)$')

    def test_view_pathargs(self):
        """Should pass uri args to view function"""
        @self.router.route('/songs/<name>')
        def sing(request, name=None):
            return name
        req = Request.blank('/songs/daisy')
        resp = req.get_response(self.router)
        self.assertEqual(resp.body, 'daisy')

    def test_uri_query(self):
        """Should pass query args to view function"""
        @self.router.route('/tada')
        def dofoo(request):
            foo = request.GET.get('foo')
            return foo
        req = Request.blank('/tada?foo=bar')
        resp = req.get_response(self.router)
        self.assertEqual(resp.body, 'bar')


def suite():
    # TODO: implement test harvester
    suite = TestLoader().loadTestsFromTestCase(TestHelpers)
    return suite
