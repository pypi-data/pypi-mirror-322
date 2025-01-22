#!/usr/bin/env python3
"""
Test text loaders.
"""

import unittest

from dalood.exception import LoaderValueError
from dalood.loader.text import TextFileLoader, TextUrlLoader
from dalood.manager import Manager


from test_dalood.utils import tmp_file


class TestText(unittest.TestCase):
    """
    Test text loading.
    """

    def test_text_file_load(self):
        """
        Text is loaded from files.
        """
        man = Manager()
        man.register_loader(r"^.*\.txt$", TextFileLoader())
        with tmp_file() as (text, _, path):
            self.assertEqual(text, man.get(path))

    def test_text_file_mtime(self):
        """
        Text file modification time is correct.
        """
        man = Manager()
        man.register_loader(r"^.*\.txt$", TextFileLoader())
        with tmp_file() as (_, mtime, path):
            self.assertEqual(mtime, man.get_mtime(path))

    def test_uri_file_load(self):
        """
        Text is loaded from URIs.
        """
        man = Manager()
        man.register_loader(r"^file://.*$", TextUrlLoader())
        with tmp_file() as (text, _, path):
            self.assertEqual(text, man.get(path.as_uri()))

    def test_text_uri_mtime(self):
        """
        Text URI modification time is correct.
        """
        man = Manager()
        man.register_loader(r"^file://.*$", TextUrlLoader())
        with tmp_file() as (_, mtime, path):
            self.assertEqual(mtime.replace(microsecond=0), man.get_mtime(path.as_uri()))

    def test_patterns(self):
        """
        Text file loader registers its own patterns.
        """
        man = Manager()
        loader = TextFileLoader()
        with tmp_file() as (text, _, path):
            with self.assertRaises(LoaderValueError):
                man.get(path.as_uri())

            loader.register_patterns(man)
            self.assertEqual(text, man.get(path))


if __name__ == "__main__":
    unittest.main()
