# -*- coding: utf-8 -*-
from unittest import TestCase

from cauliflower.forge import StorageForge


class TestStorageForge(TestCase):

    def setUp(self):
        self.storage_forge = StorageForge()

    def tearDown(self):
        del self.storage_forge

    def test_adapter_loading(self):
        """Should load storage adapters by default config"""
        storage = self.storage_forge.build()
