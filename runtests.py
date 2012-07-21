# -*- coding: utf-8 -*-
"""

Test runner which uses unittest ``discover`` method to find all
tests within ``cauliflower.testsuite`` and run them.

"""
import os
import sys

# TODO: try to import unittest2 for python2.4-2.6 backward compatability
from unittest import TextTestRunner, defaultTestLoader


if __name__ == '__main__':
    all_tests = defaultTestLoader.discover('testsuite')
    TextTestRunner(verbosity=1).run(all_tests)
