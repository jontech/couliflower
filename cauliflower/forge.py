"""Forge module

Central place where every config-related instances gets created. All config
validations required for instance creation are done here.

"""
import os
import sys

from cauliflower import config


class StoreConfigError(Exception):
    """Storage specific error"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class StorageForge(object):
    """Forge used to build Storage instances"""

    def __new__(cls):
        """Creates new storage and returns it also ensures config validity"""
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
        """Here we load our storage adapter

        :param: adapter_name - as string of adapter name
        :param: adapters_dir - as string path to dir where storage adapters are
        :param: adaper_conf - as dict holding database access settings

        :returns: Adapter instance as storage

        """
        full_adapter_name = adapter_name + '_adapter'
        adapter_toimport = '.'.join((adapters_dir, full_adapter_name))
        __import__(adapter_toimport)
        module = sys.modules[adapter_toimport]
        Adapter = getattr(module, 'Adapter')
        return Adapter(**adapter_conf)
