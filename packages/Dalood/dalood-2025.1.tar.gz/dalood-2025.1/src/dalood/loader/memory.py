#!/usr/bin/env python3
"""
Loader for objects in memory.
"""

import logging


from ..exception import ExpectedExceptionContext
from .map import MapLoaderBase


LOGGER = logging.getLogger(__name__)


class MemoryLoader(MapLoaderBase):
    """
    Loader for object in memory. This simply provided a uniform API for
    accessing objects already in memory such as those passed in by the user. In
    this case, the mapping of the parent MapLoaderBase class will map source
    arguments directly to returned data.
    """

    def load(self, src):
        with ExpectedExceptionContext(KeyError):
            return self.mapping[src]
