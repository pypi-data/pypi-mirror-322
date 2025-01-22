#!/usr/bin/env python3
"""
Test JSON loaders.
"""

import json
import unittest

from dalood.exception import LoaderValueError
from dalood.loader.json import JSONFileLoader, JSONUrlLoader
from dalood.manager import Manager


from test_dalood.utils import tmp_file


JSON_EXT = ".json"


def _get_json():
    """
    Get data and its JSON representation.
    """
    data = {"foo": 1, "bar": 2, "items": [3, 4, 5], "bool": True}
    return data, json.dumps(data)


class TestJSON(unittest.TestCase):
    """
    Test JSON loading.
    """

    def setUp(self):
        self.data, self.json_txt = _get_json()
        self.tmp_file_ctx = tmp_file(text=self.json_txt, extension=JSON_EXT)

    def test_json_file_load(self):
        """
        JSON is loaded from files.
        """
        man = Manager()
        man.register_loader(rf"^.*\{JSON_EXT}$", JSONFileLoader())
        with self.tmp_file_ctx as (_, _, path):
            self.assertEqual(self.data, man.get(path))

    def test_uri_file_load(self):
        """
        JSON is loaded from URIs.
        """
        man = Manager()
        man.register_loader(r"^file://.*$", JSONUrlLoader())
        with self.tmp_file_ctx as (_, _, path):
            self.assertEqual(self.data, man.get(path.as_uri()))

    def test_patterns(self):
        """
        JSON file loader registers its own patterns.
        """
        man = Manager()
        loader = JSONFileLoader()
        with self.tmp_file_ctx as (_, _, path):
            with self.assertRaises(LoaderValueError):
                man.get(path.as_uri())

            loader.register_patterns(man)
            self.assertEqual(self.data, man.get(path))


if __name__ == "__main__":
    unittest.main()
