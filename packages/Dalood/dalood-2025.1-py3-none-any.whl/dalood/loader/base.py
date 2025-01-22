#!/usr/bin/env python3
"""
Data loader base class.
"""

from abc import ABC, abstractmethod


class LoaderBase(ABC):
    """
    Base class for loading data from URIs or filepaths.
    """

    @abstractmethod
    def load(self, src):
        """
        Load data from the given source.

        Args:
            src:
                The data source. For some loaders this may simply be a file path
                or URI. For others it may be an arbitrary string that only has
                meaning to the loader. For example, some loaders can map
                user-defined strings to pre-defined static data, or SQL
                statements that can be used to retrieve a Pandas DataFrame from
                an open database connection.

        Returns:
            The loaded data in a form appropriate for the loader.
        """

    def get_mtime(self, src):  # pylint: disable=unused-argument
        """
        Attempt to determine the last modification time of the source.

        Args:
            src:
                The data source (e.g. a file path or URI).

        Returns:
            A datetime.datetime object representing the last known modification
            time, or None if the time cannot be determined.
        """
        return None

    @property
    def patterns(self):
        r"""
        An iterator over 2-tuples of patterns and their PatternType associated
        with this loader. For example, a text file loader might return the
        2-tuple (r"^(?!https?://).*\.txt$", PatternType.REGEX) to load local
        files by the ".txt" extenstion.
        """
        yield from []

    def register_patterns(self, manager, prioritize=False):
        """
        Register this loader with a manager for each of its common patterns.

        Args:
            manager:
                An instance of Manager.

            prioritize:
                If True, ensure that this loaders patterns take precedence over
                existing patterns in the manager.
        """
        if prioritize:
            for pattern in reversed(list(self.patterns)):
                manager.register_loader(pattern, self, prioritize=prioritize)
        else:
            for pattern in self.patterns:
                manager.register_loader(pattern, self)
