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
        field = self._introspect(name=name)
        if field:
            field = field[name].put_value(value)
        else:
            super(Model, self).__setattr__(name, value)

    def __init__(self):
        forge = StorageForge()
        self.storage = forge.build()
        self.name = self.__class__.__name__.lower()

    def save(self):
        values = []
        for name, field in self.fields.items():
            attr = getattr(self, name)
            # TODO: check type, if exists
            values.append(attr)
        self.storage.save(values)

    def sync(self):
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
