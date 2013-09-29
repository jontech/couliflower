"""Model module

Model is used to hold all the logic required to store and manage data which
could be later accessed using model's methods.

Model uses Adapters (or storage back-ends if you will) for accessing storages
like databases. For more about adapters see cauliflower/adapters package.

Here one can also find Filed implementation which is used within model to
abstract data types and pass on to Adapters.

"""
from copy import copy

from cauliflower.forge import StorageForge



class Field(object):
    """Implements abstract data-types

    Fields abstracts data type where it gets validated.

    """

    def __init__(self, field_type):
        """Prepares Field for data holding and validation

        :param: field_type - as string defines data type

        """
        self._field_type = field_type

    @classmethod
    def string(cls):
        """Creates Field instance with ``string`` data type"""
        return cls('string')

    @classmethod
    def numeric(cls):
        """Creates Field instance with ``numeric`` data type"""
        return cls('numeric')

    @classmethod
    def boolean(cls):
        """Creates Field instance with ``boolean`` data type"""
        return cls('boolean')

    @property
    def field_type(self):
        return self._field_type

    @property
    def value(self):
        return self._value

    def put_value(self, value):
        """Sets data value for Field

        also validations are made against data type of the Field

        """
        if self._field_type == 'string':
            self._value = str(value)
        else:
            self._value = value


class Model(object):
    """Provides Model for storing and managing data

    to initiate model one needs to subclass from Model class and use
    Field class data-type-methods to define Model. This alows data
    validation and control when assigning values to Model instance.

    Also this class implements ``sync`` method which synchronises
    data schema with actual data storage.

    """

    def __setattr__(self, name, value):
        """Here we actually put data value to Field according attribute

        :param: name - string name of an instance attribute
        :param: value - data value which gets passed to Field

        """
        field = self._introspect(name=name)
        if field:
            field = field[name].put_value(value)
        else:
            super(Model, self).__setattr__(name, value)

    def __init__(self, **values):
        """During initializationdf  it is possible to set all Fields

        To set Field values during Model initialization time a dict
        of field names and values is required in such form:

            {<field-name>: <value>}

        """
        if values:
            for name, value in values.items():
                field = getattr(self, name)
                field.put_value(value)
        self.storage = StorageForge()

    def save(self):
        """Here is where value of Field gets stored in actual storage

        All Field values are collected here and passed to storage
        back-end where these get saved according to earlier Model
        definition which was synced with storage.

        """
        values = []
        fields = self._introspect()
        for name, field in fields.items():
            attr = getattr(self, name)
            values.append(attr)
        model_name = self.get_model_name()
        self.storage.save(model_name, values)

    @classmethod
    def filter(cls, **query_args):
        """Finds data entries from storage as list of Model instances

        :param: query_args - a dict holding query conditions like {'id': 123}
        :returns: list with Model instances or empty list if no match

        """
        retval = []
        storage = StorageForge()
        model_name = cls.get_model_name()
        values_list = storage.filter(model_name, **query_args)
        for values in values_list:
            inst = cls(**values)
            retval.append(inst)
        return retval

    @classmethod
    def sync(cls):
        """Synchronizes Model with Storage"""
        fields = cls._introspect()
        storage = StorageForge()
        model_name = cls.get_model_name()
        storage.sync(model_name, fields)

    @classmethod
    def flush(cls):
        """Deletes all Model entries in storage"""
        fields = cls._introspect()
        storage = StorageForge()
        model_name = cls.get_model_name()
        storage.flush(model_name)

    @classmethod
    def _introspect(cls, name=None):
        """Looks for defined Field in the Model definition

        :param: name - string name of specific Field (optional)
        :returns: dict of Fields or one Field if ``name`` given

        """
        fields = {}
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, Field):
                if name is not None:
                    if attr_name == name:
                        return {attr_name: attr}
                else:
                    fields[attr_name] = attr
        return fields

    @classmethod
    def get_model_name(cls):
        """Gets name of model in lower case

        :returns: name - string name of the model

        """
        return cls.__name__.lower()
