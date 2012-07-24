# -*- coding: utf-8 -*-
from unittest import TestCase

from cauliflower.forge import StorageForge


class TestStorageForge(TestCase):

    def test_adapter_loading(self):
        """Should load storage adapters by default config"""
        storage = StorageForge()
