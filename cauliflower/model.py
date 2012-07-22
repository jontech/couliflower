# -*- coding: utf-8 -*-
from cauliflower.forge import StorageForge


def string_field(**kwargs):
    return Field('string', **kwargs)


def numeric_field(**kwargs):
    return Field('numeric', **kwargs)


def boolean_field(**kwargs):
    return Field('boolean', **kwargs)


class Field(object):

    def __init__(self, field_type, **kwargs):
        self.field_type = field_type
        attributes = kwargs


class Model(object):

    def __init__(self):
        self.fields = {}
        forge = StorageForge()
        self.storage = forge.build()
        self._introspect()

    def _introspect(self):
        """Finds properties and registers them to use within adapter"""
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, Field):
                if attr_name not in self.fields:
                    self.fields[attr_name] = attr
