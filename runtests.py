# -*- coding: utf-8 -*-
"""

Test runner which uses unittest ``discover`` method to find all
tests within ``couliflower.testsuite`` and run them.

"""
import os
import sys

# add couliflower to python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# TODO: try to import unittest2 for python2.4-2.6 backward compatability
from unittest import TextTestRunner, defaultTestLoader


if __name__ == '__main__':
    all_tests = defaultTestLoader.discover('testsuite')
    TextTestRunner(verbosity=1).run(all_tests)
