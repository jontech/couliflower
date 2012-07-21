# -*- coding: utf-8 -*-
"""

Test runner which uses unittest ``discover`` method to find all
tests within ``cauliflower.testsuite`` and run them.

"""
import sys
import argparse

# TODO: try to import unittest2 for python2.4-2.6 backward compatability
from unittest import TextTestRunner, defaultTestLoader


TESTSUITE_DIR = 'testsuite'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Yes! It runs the test in testsuite")
    parser.add_argument('--test', help="which test to run (dotted test path)")
    args = parser.parse_args()
    test = args.test

    if test:
        path = '.'.join((TESTSUITE_DIR, test))
        test_suite = defaultTestLoader.loadTestsFromName(path)
    else:
        test_suite = defaultTestLoader.discover(TESTSUITE_DIR)
    TextTestRunner(verbosity=1).run(test_suite)
