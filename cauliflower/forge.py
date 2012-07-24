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

    def __new__(cls):
        """load configuration configuration needed for storage adapter loading"""
        adapters_dir = 'cauliflower.adapters'
        try:
            adapter_name = config.STORAGE_NAME
            adapter_conf = config.STORAGE_CONF
        except AttributeError as e:
            missing = str(e).split()[-1]
            raise StoreConfigError("Missing {0} configuration".format(missing))
        storage = cls._load_adapter(adapter_name, adapters_dir, adapter_conf)
        return storage

    @classmethod
    def _load_adapter(cls, adapter_name, adapters_dir, adapter_conf):
        """Attempt to load storage adapter using configuration and pass
        it to return.
        """
        full_adapter_name = adapter_name + '_adapter'
        adapter_toimport = '.'.join((adapters_dir, full_adapter_name))
        __import__(adapter_toimport)
        module = sys.modules[adapter_toimport]
        Adapter = getattr(module, 'Adapter')
        return Adapter(**adapter_conf)
