# -*- coding: utf-8 -*-
from unittest import TestCase

from cauliflower.model import Model, Field
from cauliflower.model import string_field, boolean_field, numeric_field 


class Cup(Model):

    color = string_field()
    has_handle = boolean_field()
    capacity = numeric_field()


class TestModel(TestCase):

    def setUp(self):
        self.cup = Cup()
        self.cup.sync()

    def tearDown(self):
        del self.cup

    def test_intropsect(self):
        """Should find out all model Field attributes"""
        fields = self.cup._introspect()
        self.assertEqual(fields['color'], self.cup.color)
        self.assertEqual(fields['has_handle'], self.cup.has_handle)
        self.assertEqual(fields['capacity'], self.cup.capacity)

    def test_name_introspect(self):
        """Should find one model Field attribute"""
        field = self.cup._introspect(name='color')
        self.assertTrue(isinstance(field['color'], Field))
        self.assertEqual(field['color']._field_type, 'string')

    def test_set_field_value(self):
        """Should put value 'red' into Field object"""
        self.cup.color = 'red'
        self.assertEqual(self.cup.color.value, 'red')

    def test_save(self):
        """Should save data by model"""
        # create red cup
        self.cup.color = 'red'
        self.cup.has_handle = 'true'
        self.cup.capacity = 250
        self.cup.save()

        # now create green cup
        self.cup.color = 'green'
        self.cup.has_handle = 'false'
        self.cup.capacity = 120
        self.cup.save()
