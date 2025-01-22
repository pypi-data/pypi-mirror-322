#!/usr/bin/env python3
"""
YAML data loaders.
"""

import yaml

from ..exception import ExpectedExceptionContext
from ..regex import get_extension_pattern_for_filepath
from .file import FileLoaderBase
from .url import UrlLoaderBase


ExpectedExceptionContext.map_exception(yaml.YAMLError, ValueError)


class YAMLFileLoader(FileLoaderBase):
    """
    YAML file data loader.
    """

    def __init__(self, encoding="utf-8"):
        """
        Args:
            encoding:
                The file encoding.
        """
        super().__init__("r", encoding=encoding)

    def load(self, src):
        with self.stream(src, yaml.YAMLError) as handle:
            return yaml.safe_load(handle)

    @property
    def patterns(self):
        yield get_extension_pattern_for_filepath(r"\.ya?ml", escape=False)


class YAMLUrlLoader(UrlLoaderBase):
    """
    YAML URL data loader.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def load(self, src):
        with self.stream(src, yaml.YAMLError) as resp:
            return yaml.safe_load(resp.raw)
