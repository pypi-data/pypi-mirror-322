#!/usr/bin/env python3
"""
Base class for other file loaders.
"""

import contextlib
import datetime
import logging
import pathlib

from ..exception import ExpectedExceptionContext
from .base import LoaderBase


LOGGER = logging.getLogger(__name__)


class FileLoaderBase(LoaderBase):
    """
    Base class for loading data from files.
    """

    DEFAULT_ENCODING = "utf-8"

    def __init__(self, *args, **kwargs):
        """
        Args:
            *args:
                Positional arguments passed through to pathlib.open after the
                path.

            **kwargs:
                Keyword arguments passed through to pathlib.open.
        """
        self.args = args
        self.kwargs = kwargs

    @contextlib.contextmanager
    def stream(self, src, *exceptions):
        """
        Context manager for accessing the open file buffer.
        """
        path = pathlib.Path(src).resolve()
        args = self.args if self.args else ["rb"]
        kwargs = {**self.kwargs}
        if args[0] == "r":
            kwargs.setdefault("encoding", self.DEFAULT_ENCODING)

        LOGGER.debug("Opening %s with %s, %s", path, args, kwargs)
        with ExpectedExceptionContext(
            OSError, *exceptions, error_msg=f"Failed to open {path}"
        ):
            with path.open(  # pylint: disable=unspecified-encoding
                *args, **kwargs
            ) as handle:
                yield handle

    def get_mtime(self, src):
        path = pathlib.Path(src).resolve()
        with ExpectedExceptionContext(OSError):
            mtime = path.stat().st_mtime
        return datetime.datetime.fromtimestamp(mtime, datetime.timezone.utc)
