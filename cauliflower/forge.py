# -*- coding: utf-8 -*-
import os
import sys

from cauliflower import config


class StoreConfigError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class Forge(object):

    def build(self):
        raise NotImplementedError("build should be implemented in subclass")

    def rebuild(self):
        raise NotImplementedError("rebuild should be implemented in subclass")


class StorageForge(Forge):

    def __init__(self):
        """load configuration configuration needed for storage adapter loading"""
        self.adapters_dir = 'cauliflower.adapters'
        try:
            self.adapter_name = config.STORAGE_NAME
        except AttributeError as e:
            missing = str(e).split()[-1]
            raise StoreConfigError("Missing {0} configuration".format(missing))

    def build(self):
        """Attempt to load storage adapter using configuration and pass
        it to return.
        """
        adapter_toimport = '.'.join((self.adapters_dir, self.adapter_name))
        __import__(adapter_toimport)
        module = sys.modules[adapter_toimport]
        print module
        adapter = getattr(module, 'Adapter')
        return adapter()
