#!/usr/bin/env python3
"""
Regular expression types and functions.
"""

import enum
import fnmatch
import logging
import re


LOGGER = logging.getLogger(__name__)


@enum.unique
class PatternType(enum.Enum):
    """
    Recognized pattern types.
    """

    REGEX = enum.auto()
    GLOB = enum.auto()
    LITERAL = enum.auto()

    @classmethod
    def from_str(cls, arg):
        """
        Convert a string to a PatternType.
        """
        arg = str(arg).upper()
        for ptype in cls:
            if ptype.name == arg:
                return ptype
        raise ValueError(f"Unrecognized pattern type: {arg}")


class RegexPattern:  # pylint: disable=too-few-public-methods
    """
    Regular expression pattern.
    """

    TYPE = PatternType.REGEX

    def __init__(self, pattern, flags=0):
        if not isinstance(pattern, re.Pattern):
            pattern = re.compile(pattern, flags=flags)
        self.regex = pattern
        self.pattern = self.regex.pattern

    def fullmatch(self, *args, **kwargs):
        """
        Wrapper around re.Pattern.fullmatch
        """
        return self.regex.fullmatch(*args, **kwargs)


class GlobPattern(RegexPattern):  # pylint: disable=too-few-public-methods
    """
    Glob pattern.
    """

    TYPE = PatternType.GLOB

    def __init__(self, pattern):
        super().__init__(fnmatch.translate(pattern))
        self.pattern = pattern


class LiteralPattern(RegexPattern):  # pylint: disable=too-few-public-methods
    """
    Literal pattern.
    """

    TYPE = PatternType.LITERAL

    def __init__(self, pattern):
        super().__init__(re.escape(pattern))
        self.pattern = pattern


def get_regex(pattern, pattern_type=PatternType.REGEX):
    """
    Get the regular expression corresponding to the given pattern.

    Args:
        pattern:
            A string containing a pattern of the specified type that should be
            converted to a regular expression.

        pattern_type:
            An instance of :py:class:`~.PatternType` or an equivalent string.

    Returns:
        An re.Pattern regular expression object.
    """
    if isinstance(pattern, RegexPattern):
        return pattern

    if isinstance(pattern_type, str):
        pattern_type = PatternType.from_str(pattern_type)

    if pattern_type is PatternType.LITERAL:
        return LiteralPattern(pattern)

    if pattern_type is PatternType.GLOB:
        return GlobPattern(pattern)

    if pattern_type is PatternType.REGEX:
        return RegexPattern(pattern)

    raise ValueError(f"Unrecogznied pattern type: {pattern_type}")


def get_extension_pattern_for_filepath(ext, escape=True):
    r"""
    Get a regular expression pattern for filepaths that end with the given
    extension. This will exclude URIs, including file URIs.

    Args:
        ext:
            The extention to recognize, e.g. ".txt".

        escape:
            If True, escape the extension for the pattern. This can be set to
            false whena pre-escaped pattern is passed in, e.g. r"\.[tc]sv".

    Returns:
        A RegexPattern or a subclass thereof.
    """
    if escape:
        ext = re.escape(ext)
    return RegexPattern(rf"^(?!\w+://).*{ext}$")
