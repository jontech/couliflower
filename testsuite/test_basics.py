# -*- coding: utf-8 -*-
import types
from unittest import TestCase, TestLoader

from couliflower.router import build_route, Router
from couliflower.helpers import load_view, view


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
        expected = '^\/a\/static\/path$'
        self.assertEqual(res, expected)

    def test_arg_in_path(self):
        """Should make re to match args in URI path"""
        res = build_route('/<foo>')
        expected = '^\\/(?P<foo>[^/]+)$'
        self.assertEqual(res, expected)

    def test_arg_validation(self):
        """Should verify path argument as string length 16"""
        # TODO: not implemented
        pat = '/<string:foo[16]>'
        pass


class TestRouting(TestCase):
    """Test the routing from URI to view loaded"""

    def setUp(self):
        self.router = Router()

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


    def test_specific_view(self):
        """Should load specific view"""
        pass

    def test_path_args(self):
        """Should load specific view and pass path arg"""
        pass


def suite():
    # TODO: implement test harvester
    suite = TestLoader().loadTestsFromTestCase(TestHelpers)
    return suite
