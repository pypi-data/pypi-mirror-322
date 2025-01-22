#!/usr/bin/env python3
"""
Text data loaders.
"""

import logging

from ..regex import get_extension_pattern_for_filepath
from .file import FileLoaderBase
from .url import UrlLoaderBase


LOGGER = logging.getLogger(__name__)


class TextFileLoader(FileLoaderBase):
    """
    Text file data loader.
    """

    def __init__(self, encoding="utf-8"):
        """
        Args:
            encoding:
                The file encoding.
        """
        super().__init__("r", encoding=encoding)

    def load(self, src):
        with self.stream(src) as handle:
            return handle.read()

    @property
    def patterns(self):
        yield get_extension_pattern_for_filepath(".txt")


class TextUrlLoader(UrlLoaderBase):
    """
    Text URL data loader.
    """

    def __init__(self, *args, encoding="utf-8", **kwargs):
        """
        Args:
            encoding:
                The stream encoding.
        """
        super().__init__(*args, **kwargs)
        self.encoding = encoding

    def load(self, src):
        with self.stream(src) as resp:
            text = resp.content
            if self.encoding is not None:
                return text.decode(self.encoding)
            return text
