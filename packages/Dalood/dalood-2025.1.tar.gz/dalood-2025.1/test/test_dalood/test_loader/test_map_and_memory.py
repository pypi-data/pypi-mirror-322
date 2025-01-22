#!/usr/bin/env python3
"""
Test map and memory loader.
"""

import json
import unittest

from dalood.loader.memory import MemoryLoader
from dalood.manager import Manager


class TestMemory(unittest.TestCase):
    """
    Test memory loading.
    """

    def setUp(self):
        self.man = Manager()
        self.data = {
            "test1": ("a", 1),
            "test2": ("b", 2),
        }

    def test_init_mapping(self):
        """
        Mapping is recognized when passed to __init__.
        """
        loader = MemoryLoader(mapping=self.data)
        loader.register_patterns(self.man)
        for name, data in self.data.items():
            with self.subTest(name=name):
                self.assertEqual(data, self.man.get(name))

    def test_map_method(self):
        """
        Mapping via map function works.
        """
        loader = MemoryLoader()
        for name, data in self.data.items():
            loader.map(name, data)
        loader.register_patterns(self.man)
        for name, data in self.data.items():
            with self.subTest(name=name):
                self.assertEqual(data, self.man.get(name))


if __name__ == "__main__":
    unittest.main()
