#!/usr/bin/env python3
"""
Pandas dataframe loaders
"""

import logging

import pandas as pd

from ..exception import ExpectedExceptionContext
from ..regex import get_extension_pattern_for_filepath
from .file import FileLoaderBase
from .map import MapLoaderBase


LOGGER = logging.getLogger(__name__)


class DataFrameCSVLoader(FileLoaderBase):
    """
    CSV & TSV file dataframe loader.
    """

    def __init__(self, **kwargs):
        """
        Args:
            **kwargs:
                Keyword arguments for pandas.read_csv().
        """
        super().__init__()
        self.kwargs = kwargs

    def load(self, src):
        src = str(src)
        LOGGER.debug("Loading Pandas dataframe from %s", src)
        with ExpectedExceptionContext(OSError, ValueError):
            return pd.read_csv(src, **self.kwargs)

    @property
    def patterns(self):
        yield get_extension_pattern_for_filepath(r"\.[ct]sv", escape=False)


class DataFrameSQLLoader(MapLoaderBase):
    """
    Text URL data loader.
    """

    def __init__(self, mapping=None, **kwargs):
        """
        Args:
            mapping:
                A dict mapping the source arguments to SQL statements. When a
                source is requested, the mapped SQL statement will be passed
                through to pandas.read_sql() along with the keyword arguments in
                kwargs.

            **kwargs:
                Keyword arguments for pandas.read_sql().
        """
        super().__init__(mapping=mapping)
        self.kwargs = kwargs

    def load(self, src):
        src = str(src)
        LOGGER.debug("Loading Pandas dataframe from %s", src)
        with ExpectedExceptionContext(OSError, ValueError, KeyError):
            sql = self.mapping[src]
            return pd.read_sql(sql, **self.kwargs)
