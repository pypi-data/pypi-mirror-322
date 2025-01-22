#!/usr/bin/env python3
"""
JSON data loaders.
"""

import json

from ..exception import ExpectedExceptionContext
from ..regex import get_extension_pattern_for_filepath
from .file import FileLoaderBase
from .url import UrlLoaderBase


ExpectedExceptionContext.map_exception(json.JSONDecodeError, ValueError)


class JSONFileLoader(FileLoaderBase):
    """
    JSON file data loader.
    """

    def __init__(self):
        super().__init__("rb")

    def load(self, src):
        with self.stream(src, json.JSONDecodeError) as handle:
            return json.load(handle)

    @property
    def patterns(self):
        yield get_extension_pattern_for_filepath(".json")


class JSONUrlLoader(UrlLoaderBase):
    """
    JSON URL data loader.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def load(self, src):
        with self.stream(src) as resp:
            return resp.json()
