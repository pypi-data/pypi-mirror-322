#!/usr/bin/env python3
"""
Test regex module.
"""

import datetime
import unittest

from dalood.regex import (
    PatternType,
    RegexPattern,
    GlobPattern,
    LiteralPattern,
    get_regex,
)


class TestGetRegex(unittest.TestCase):
    """
    Test get_regex function.
    """

    def test_passthrough(self):
        """
        RegexPattern instances are returned.
        """
        for pattern in (
            RegexPattern(r".*\.txt$"),
            GlobPattern(r"*.json"),
            LiteralPattern("foo.yaml"),
        ):
            self.assertIs(pattern, get_regex(pattern))

    def test_regex_type(self):
        """
        RegexPatterns are returned.
        """
        pattern = get_regex("f.o", pattern_type="regex")
        self.assertIs(pattern.__class__, RegexPattern)
        self.assertEqual(pattern.regex.pattern, r"f.o")

    def test_glob_type(self):
        """
        GlobPatterns are returned.
        """
        pattern = get_regex("f*o", pattern_type="glob")
        self.assertIs(pattern.__class__, GlobPattern)
        self.assertEqual(pattern.regex.pattern, r"(?s:f.*o)\Z")

    def test_literal_type(self):
        """
        LiteralPatterns are returned.
        """
        pattern = get_regex("f?o", pattern_type="literal")
        self.assertIs(pattern.__class__, LiteralPattern)
        self.assertEqual(pattern.regex.pattern, r"f\?o")

    def test_invalid_pattern_types(self):
        """
        Invalid pattern types raise errors.
        """
        for invalid_type in ("globx", None, 5, False):
            with self.subTest(invalid_type=invalid_type), self.assertRaises(ValueError):
                get_regex("foo", pattern_type=invalid_type)


if __name__ == "__main__":
    unittest.main()
