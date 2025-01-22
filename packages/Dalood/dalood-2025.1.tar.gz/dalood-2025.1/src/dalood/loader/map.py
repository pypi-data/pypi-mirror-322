#!/usr/bin/env python3
"""
Base class for loaders that map sources to data via a user-defined map.
"""

import logging


from ..regex import LiteralPattern
from .base import LoaderBase


LOGGER = logging.getLogger(__name__)


class MapLoaderBase(LoaderBase):
    """
    Base class for loaders that map sources to data via a user-defined map.
    """

    def __init__(self, mapping=None):
        """
        Args:
            mapping:
                A dict mapping the source arguments to user-defined data. How
                that data is used will be determined by the implementation of
                load and get_mtime in derived classes. For example, for a loader
                that loads Pandas DataFrames from a database, the mapping could
                map source arguments to SQL statements that are passed through
                to pandas.read_sql.
        """
        super().__init__()
        if mapping is None:
            mapping = {}
        self.mapping = mapping

    def map(self, src, value):
        """
        Map a source to a value in the internal mapping.

        Args:
            src:
                The source to map.

            value:
                The value to which to map the source.
        """
        self.mapping[src] = value

    @property
    def patterns(self):
        for key in self.mapping:
            yield LiteralPattern(key)
