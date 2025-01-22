#!/usr/bin/env python3
"""
Data wrapper class.
"""

import datetime
import logging

LOGGER = logging.getLogger(__name__)


class DataWrapper:
    """
    Wrapper around loaded data that stores that data and a loader reference, and
    tracks loading and access times.
    """

    def __init__(self, loader, src):
        self.loader = loader
        self.src = src
        self.data = None
        self.load_time = None
        self.access_time = None

    @staticmethod
    def _now():
        """
        Get the current datetime in the UTC timezone.
        """
        return datetime.datetime.now(datetime.timezone.utc)

    def load(self):
        """
        Load the data for the given source.

        Args:
            src:
                The data source (e.g. a file or URI, or whatever else the
                matching loader can handle).
        """
        self.data = self.loader.load(self.src)
        self.load_time = self._now()
        self.access_time = self.load_time

    def refresh(self):
        """
        Reload data if the loader reports that the data has changed since it was
        last loaded.
        """
        mtime = self.loader.get_mtime(self.src)
        if mtime is not None and mtime > self.load_time:
            LOGGER.debug("Refreshing %s", self.src)
            self.load()

    def access(self):
        """
        Access the data. It will be loaded first if necessary.
        """
        if self.load_time is None:
            self.load()
        self.access_time = self._now()
        return self.data
