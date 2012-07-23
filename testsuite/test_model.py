# -*- coding: utf-8 -*-
from unittest import TestCase

from cauliflower.model import Model, Field


class Cup(Model):
    """Test Model with some fields also to test"""

    color = Field.string()
    has_handle = Field.boolean()
    capacity = Field.numeric()


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

    def test_filter_everything(self):
        """Should get all records for given Model"""
        cups = self.cup.filter()
        self.assertEqual(cups[0].color.value, 'green')
        self.assertEqual(cups[0].has_handle.value, 'false')
        self.assertEqual(cups[0].capacity.value, 120)

    def test_filter_by_color(self):
        """Should get only red cups"""
        cups = self.cup.filter(color='red')
        self.assertEqual(cups[0].color.value, 'red')
        self.assertEqual(cups[1].color.value, 'red')
        self.assertEqual(cups[3].color.value, 'red')
