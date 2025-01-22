#!/usr/bin/env python3
"""
Test Manager.
"""

import datetime
import unittest
import re
from unittest.mock import MagicMock

from dalood.loader.text import TextFileLoader
from dalood.manager import Manager
from dalood.regex import PatternType, GlobPattern


from test_dalood.utils import tmp_file


TEXT_EXT = ".txt"


def shift_times(manager):
    """
    Shift load times one day into the past and access times 6 hours into the
    past for all loaded data in the manager.

    Args:
        manager:
            A Manager instance.
    """
    load_delta = datetime.timedelta(days=1)
    access_delta = datetime.timedelta(hours=6)
    for wrapper in manager._cache.values():  # pylint: disable=protected-access
        wrapper.load_time -= load_delta
        wrapper.access_time -= access_delta


class TestManager(unittest.TestCase):
    """
    Test Manager class.
    """

    def setUp(self):
        self.text = "placeholder text"
        self.tmp_file_ctx = tmp_file(text=self.text, extension=TEXT_EXT)

        self.man = Manager()
        self.loader = TextFileLoader()
        self.man.register_loader(rf"^.*\{TEXT_EXT}$", self.loader)

    def _pattern_iterator(self):
        """
        Common convenience method for testing pattern types.
        """
        with self.tmp_file_ctx as (text, mtime, path):
            for name, pattern in (
                ("glob", f"*{TEXT_EXT}"),
                ("literal", str(path)),
                ("regex", rf"^.*{re.escape(TEXT_EXT)}$"),
            ):
                yield text, mtime, path, name, pattern

    def test_register_loader_with_x_pattern(self):
        """
        Convenience wrappers around register_loader work.
        """
        for text, _, path, name, pattern in self._pattern_iterator():
            with self.subTest(name=name, pattern=pattern):
                self.man.loaders.clear()
                getattr(self.man, f"register_loader_with_{name}_pattern")(
                    pattern, TextFileLoader()
                )
                self.assertEqual(text, self.man.get(path))

    def test_get_loader(self):
        """
        Manager returns loader.
        """
        self.assertEqual(self.loader, self.man.get_loader(f"foo{TEXT_EXT}"))

    def test_clear_cache(self):
        """
        Manager clears cached data.
        """
        with self.tmp_file_ctx as (_, _, path):
            # Clear all.
            self.man.get(path)
            self.assertEqual([str(path)], list(self.man))
            self.man.clear_cache()
            self.assertEqual([], list(self.man))

            # Clear by load time.
            self.man.get(path)
            shift_times(self.man)
            self.assertEqual([str(path)], list(self.man))
            self.man.clear_cache(age={"hours": 36})
            self.assertEqual([str(path)], list(self.man))
            self.man.clear_cache(age={"hours": 20})
            self.assertEqual([], list(self.man))

            # Clear by access time.
            self.man.get(path)
            shift_times(self.man)
            self.assertEqual([str(path)], list(self.man))
            self.man.clear_cache(age={"hours": 20}, by_access_time=True)
            self.assertEqual([str(path)], list(self.man))
            self.man.clear_cache(age={"hours": 3}, by_access_time=True)
            self.assertEqual([], list(self.man))

            # Clear by pattern.
            self.man.get(path)
            self.assertEqual([str(path)], list(self.man))
            self.man.clear_cache(pattern="sfdsdfsdf", pattern_type=PatternType.LITERAL)
            self.assertEqual([str(path)], list(self.man))
            self.man.clear_cache(pattern=f"*{TEXT_EXT}", pattern_type=PatternType.GLOB)
            self.assertEqual([], list(self.man))

            self.man.get(path)
            self.assertEqual([str(path)], list(self.man))
            self.man.clear_cache(pattern=GlobPattern(f"*{TEXT_EXT}"))
            self.assertEqual([], list(self.man))

    def test_clear_cache_with_x_pattern(self):
        """
        Convenience wrappers around clear_cache work.
        """
        for _, _, path, name, pattern in self._pattern_iterator():
            with self.subTest(name=name, pattern=pattern):
                self.man.get(path)
                self.assertEqual([str(path)], list(self.man))
                getattr(self.man, f"clear_cache_with_{name}_pattern")(pattern)
                self.assertEqual([], list(self.man))

    def test_refresh(self):
        """
        Manager refreshes data.
        """
        with self.tmp_file_ctx as (_, _, path):
            self.man.get(path)
            shift_times(self.man)
            wrapper = self.man._get_wrapper(path)  # pylint: disable=protected-access
            prev_load_time = wrapper.load_time
            prev_access_time = wrapper.access_time
            self.man.refresh()
            wrapper = self.man._get_wrapper(path)  # pylint: disable=protected-access
            self.assertGreater(wrapper.load_time, prev_load_time)
            self.assertGreater(wrapper.access_time, prev_access_time)

            # Refresh by pattern.
            shift_times(self.man)
            wrapper = self.man._get_wrapper(path)  # pylint: disable=protected-access
            prev_load_time = wrapper.load_time
            prev_access_time = wrapper.access_time
            self.man.refresh(pattern="sfdsdfsdf", pattern_type=PatternType.LITERAL)
            wrapper = self.man._get_wrapper(path)  # pylint: disable=protected-access
            self.assertEqual(wrapper.load_time, prev_load_time)
            self.assertEqual(wrapper.access_time, prev_access_time)

            self.man.refresh(pattern=f"*{TEXT_EXT}", pattern_type=PatternType.GLOB)
            wrapper = self.man._get_wrapper(path)  # pylint: disable=protected-access
            self.assertGreater(wrapper.load_time, prev_load_time)
            self.assertGreater(wrapper.access_time, prev_access_time)

    def test_refresh_with_x_pattern(self):
        """
        Convenience wrappers around refresh work.
        """
        for _, _, path, name, pattern in self._pattern_iterator():
            with self.subTest(name=name, pattern=pattern):
                self.man.get(path)
                shift_times(self.man)
                wrapper = self.man._get_wrapper(
                    path
                )  # pylint: disable=protected-access
                prev_load_time = wrapper.load_time
                prev_access_time = wrapper.access_time
                getattr(self.man, f"refresh_with_{name}_pattern")(pattern)
                wrapper = self.man._get_wrapper(
                    path
                )  # pylint: disable=protected-access
                self.assertGreater(wrapper.load_time, prev_load_time)
                self.assertGreater(wrapper.access_time, prev_access_time)

    def test_get(self):
        """
        Manager returns data.
        """
        with self.tmp_file_ctx as (text, _, path):
            self.assertEqual(text, self.man.get(path))

            wrapper = self.man._get_wrapper(path)  # pylint: disable=protected-access

            # Reload parameter.
            wrapper.load = MagicMock(side_effect=wrapper.load)
            self.man.get(path)
            wrapper.load.assert_not_called()
            self.man.get(path, reload=True)
            wrapper.load.assert_called()

            # Refresh parameter.
            wrapper.refresh = MagicMock(side_effect=wrapper.refresh)
            self.man.get(path)
            wrapper.refresh.assert_not_called()
            self.man.get(path, refresh=True)
            wrapper.refresh.assert_called()

    def test_get_mtime(self):
        """
        Manager returns last modification time of source.
        """
        with self.tmp_file_ctx as (_, mtime, path):
            self.assertEqual(mtime, self.man.get_mtime(path))


if __name__ == "__main__":
    unittest.main()
