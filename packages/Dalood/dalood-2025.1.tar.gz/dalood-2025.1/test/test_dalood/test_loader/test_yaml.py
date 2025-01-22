#!/usr/bin/env python3
"""
Test YAML loaders.
"""

import unittest

import yaml

from dalood.exception import LoaderValueError
from dalood.loader.yaml import YAMLFileLoader, YAMLUrlLoader
from dalood.manager import Manager


from test_dalood.utils import tmp_file


YAML_EXT = ".yaml"


def _get_yaml():
    """
    Get data and its YAML representation.
    """
    data = {"foo": 1, "bar": 2, "items": [3, 4, 5], "bool": True}
    return data, yaml.dump(data)


class TestYAML(unittest.TestCase):
    """
    Test YAML loading.
    """

    def setUp(self):
        self.data, self.yaml_txt = _get_yaml()
        self.tmp_file_ctx = tmp_file(text=self.yaml_txt, extension=YAML_EXT)

    def test_yaml_file_load(self):
        """
        YAML is loaded from files.
        """
        man = Manager()
        man.register_loader(r"^.*\.yaml$", YAMLFileLoader())
        with self.tmp_file_ctx as (_, _, path):
            self.assertEqual(self.data, man.get(path))

    def test_uri_file_load(self):
        """
        YAML is loaded from URIs.
        """
        man = Manager()
        man.register_loader(r"^file://.*$", YAMLUrlLoader())
        with self.tmp_file_ctx as (_, _, path):
            self.assertEqual(self.data, man.get(path.as_uri()))

    def test_patterns(self):
        """
        YAML file loader registers its own patterns.
        """
        man = Manager()
        loader = YAMLFileLoader()
        with self.tmp_file_ctx as (_, _, path):
            with self.assertRaises(LoaderValueError):
                man.get(path.as_uri())

            loader.register_patterns(man, prioritize=True)
            self.assertEqual(self.data, man.get(path))


if __name__ == "__main__":
    unittest.main()
