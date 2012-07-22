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
        self._field_type = field_type
        attributes = kwargs

    @property
    def field_type(self):
        return self._field_type


class Model(object):

    def __init__(self):
        forge = StorageForge()
        # TODO: would be nicer to have class method
        self.storage = forge.build()
        self.fields = self._introspect()
        self.storage.sync(self.fields)

    def _introspect(self):
        """Finds properties and registers them to use within adapter"""
        fields = {}
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, Field):
                if attr_name not in fields:
                    fields[attr_name] = attr
        return fields
