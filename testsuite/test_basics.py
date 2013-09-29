# -*- coding: utf-8 -*-
import types
from unittest import TestCase, TestLoader

from cauliflower.view import load_view, view


class TestHelpers(TestCase):
    """Check helper functions output"""

    def test_load_view(self):
        """Should load view function by string representation"""
        view = load_view('test_views:dobla')
        self.assertTrue(isinstance(view, types.FunctionType))


def suite():
    suite = TestLoader().loadTestsFromTestCase(TestHelpers)
    return suite
