# -*- coding: utf-8 -*-
from copy import copy

from cauliflower.forge import StorageForge


def string_field(**kwargs):
    return Field('string', **kwargs)


def numeric_field(**kwargs):
    return Field('numeric', **kwargs)


def boolean_field(**kwargs):
    return Field('boolean', **kwargs)


class Field(object):

    def __init__(self, field_type, **kwargs):
        """Initialize field type"""
        # TODO: check if given field type is supported
        self._field_type = field_type
        attributes = kwargs

    @property
    def field_type(self):
        return self._field_type

    @property
    def value(self):
        return self._value

    def put_value(self, value):
        """Create value for this field type"""
        self._value = value


class Model(object):

    def __setattr__(self, name, value):
        """Control Model values assignment -- if we are assigning Field
        attribute, assign value to Field else do assignment as usual.

        """
        field = self._introspect(name=name)
        if field:
            field = field[name].put_value(value)
        else:
            # TODO: raise error instead?
            super(Model, self).__setattr__(name, value)

    def __init__(self):
        forge = StorageForge()
        # TODO: fix forge build method name to build_storage
        self.storage = forge.build()
        # TODO: put this to forge build as name argument
        self.name = self.__class__.__name__.lower()

    def save(self):
        """Store Model Field values to storage"""
        values = []
        fields = self._introspect()
        for name, field in fields.items():
            attr = getattr(self, name)
            # TODO: check type, if exists
            values.append(attr)
        self.storage.save(values)

    def filter(self):
        """Gets data from storage, builds Model objects and returns list"""
        retval = []
        values_list = self.storage.filter()
        for values in values_list:
            clone = copy(self)
            fields = clone._introspect().values()
            # TODO: assure data integrity!!
            pairs = zip(fields, values)
            for field, value in pairs:
                field.put_value(value)
                retval.append(clone)
        return retval

    def sync(self):
        """Syncs storage with Model schema"""
        fields = self._introspect()
        self.storage.sync(self.name, fields)

    def _introspect(self, name=None):
        """Finds properties and registers them to use within adapter"""
        fields = {}
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, Field):
                if name is not None:
                    if attr_name == name:
                        return {attr_name: attr}
                else:
                    fields[attr_name] = attr
        return fields
