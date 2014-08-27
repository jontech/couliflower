# -*- coding: utf-8 -*-
from unittest import TestCase

from cauliflower.model import Model, Field


class Cup(Model):
    """Model to test"""

    color = Field.string()
    has_handle = Field.boolean()
    capacity = Field.numeric()


Cup.sync()


class TestModel(TestCase):

    def setUp(self):
        """Creates some cups"""
        # create red cup
        cup = Cup()
        cup.color = 'red'
        cup.has_handle = 'true'
        cup.capacity = 250
        cup.save()

        # now create green cup
        cup = Cup()
        cup.color = 'green'
        cup.has_handle = 'false'
        cup.capacity = 120
        cup.save()

    def tearDown(self):
        """Removes all cups"""
        Cup.flush() 

    def test_intropsect(self):
        """Should find out all model Field attributes"""
        cup = Cup()
        fields = cup._introspect()
        self.assertEqual(fields['color'], cup.color)
        self.assertEqual(fields['has_handle'], cup.has_handle)
        self.assertEqual(fields['capacity'], cup.capacity)

    def test_name_introspect(self):
        """Should find one model Field attribute"""
        cup = Cup()
        field = cup._introspect(name='color')
        self.assertTrue(isinstance(field['color'], Field))
        self.assertEqual(field['color']._field_type, 'string')

    def test_set_field_value(self):
        """Should put value 'red' into Field object"""
        cup = Cup()
        cup.color = 'red'
        self.assertEqual(cup.color.value, 'red')

    def test_filter_everything(self):
        """Should get all records for given Model"""
        cups = Cup.filter()
        self.assertEqual(len(cups), 2)

        self.assertEqual(cups[0].color.value, 'green')
        self.assertEqual(cups[1].color.value, 'red')

    def test_filter_by_color(self):
        """Should get only red cups"""
        # create red cup
        cup = Cup()
        cup.color = 'red'
        cup.has_handle = 'true'
        cup.capacity = 100
        cup.save()

        # create red cup
        cup = Cup()
        cup.color = 'red'
        cup.has_handle = 'true'
        cup.capacity = 120
        cup.save()

        cups = Cup.filter(color='red')
        self.assertEqual(cups[0].color.value, 'red')
        self.assertEqual(cups[1].color.value, 'red')
        self.assertEqual(cups[2].color.value, 'red')
