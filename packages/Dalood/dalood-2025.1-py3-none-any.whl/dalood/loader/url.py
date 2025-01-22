#!/usr/bin/env python3
"""
Base class for other URL loaders.
"""

import contextlib
import datetime
import logging

from requests.exceptions import RequestException
from requests_file_adapter import get_session

from ..exception import ExpectedExceptionContext, LoaderOSError
from .base import LoaderBase


LOGGER = logging.getLogger(__name__)


ExpectedExceptionContext.map_exception(RequestException, LoaderOSError)


class UrlLoaderBase(LoaderBase):
    """
    Base class for loading data from URLs. This will check modification times
    via a HEAD request.
    """

    def __init__(self, timeout=5):
        """
        Args:
            timeout:
                Timeout parameter passed through to requests.
        """
        self.timeout = timeout

    @contextlib.contextmanager
    def stream(self, src, *exceptions):
        """
        Context manager for accessing the data raw stream. It returns the
        response through which the content can be accessed.
        """
        LOGGER.debug("Getting %s", src)
        session = get_session()
        with ExpectedExceptionContext(RequestException, *exceptions):
            resp = session.get(src, timeout=self.timeout, stream=True)
            yield resp
        resp.close()

    def get_mtime(self, src):
        time_fmt = "%a, %d %b %Y %H:%M:%S %Z"
        session = get_session()
        with ExpectedExceptionContext(RequestException):
            resp = session.head(src, timeout=self.timeout)
        try:
            last_mod = resp.headers["last-modified"]
        except KeyError:
            return None
        mtime = datetime.datetime.strptime(last_mod, time_fmt)
        # strptime seems to return naive datetime objects without tzinfo
        if mtime.tzinfo is None and last_mod.endswith(" GMT"):
            mtime = mtime.replace(tzinfo=datetime.timezone.utc)
        return mtime
