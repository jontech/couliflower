# -*- coding: utf-8 -*-
from unittest import TestCase

from cauliflower.model import Model
from cauliflower.model import string_field, boolean_field, numeric_field 


class Cup(Model):

    color = string_field()
    has_handle = boolean_field()
    capacity = numeric_field()


class TestModel(TestCase):

    def setUp(self):
        self.cup = Cup()

    def tearDown(self):
        del self.cup

    def test_intropsect(self):
        """Should find out model fields"""
        fields = self.cup.fields
        self.assertEqual(fields['color'], self.cup.color)
        self.assertEqual(fields['has_handle'], self.cup.has_handle)
        self.assertEqual(fields['capacity'], self.cup.capacity)
