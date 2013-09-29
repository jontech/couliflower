import types
from unittest import TestCase, TestLoader
from webob import Request

from cauliflower.router import build_route, Router


class TestRouting(TestCase):
    """Test the routing from URI to view loaded"""

    def setUp(self):
        """Always prepare new Router instance for test"""
        self.router = Router()

    def tearDown(self):
        """Delete Router instance after test"""
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
        self.assertTrue(isinstance(res_view, types.FunctionType))
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

        request = Request.blank('/songs/daisy')

        response = request.get_response(self.router)
        self.assertEqual(response.body, 'daisy')

    def test_uri_query(self):
        """Should pass query args to view function"""

        @self.router.route('/tada')
        def dofoo(request):
            foo = request.GET.get('foo')
            return foo

        request = Request.blank('/tada?foo=bar')

        response = request.get_response(self.router)
        self.assertEqual(response.body, 'bar')

    def test_static_path(self):
        """Should create regex to match URI path without args"""
        res = build_route('/a/static/path')
        self.assertEqual(res, '^\/a\/static\/path$')

    def test_arg_in_path(self):
        """Should make re to match args in URI path"""
        res = build_route('/<foo>')
        self.assertEqual(res, '^\\/(?P<foo>[^/]+)$')

def suite():
    suite = TestLoader().loadTestsFromTestCase(TestHelpers)
    return suite
