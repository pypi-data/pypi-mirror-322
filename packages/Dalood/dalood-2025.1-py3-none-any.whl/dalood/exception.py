#!/usr/bin/env python3
"""
Custom exceptions.
"""


import sys


THIS_MODULE = sys.modules[__name__]


class LoaderError(Exception):
    """
    Custom exception base class.
    """


class ExpectedExceptionContext:
    """
    Context manager to convert expected exceptions other exception types.
    """

    # Predefined map of commonly expected exceptions to custom exception
    # subclasses.
    EXCEPTION_MAP = {}

    @classmethod
    def map_exception(cls, ex_from, ex_to):
        """
        Add an exception pair to the exception map.

        Args:
            ex_from:
                The exception to map.

            ex_to:
                The exception to which ex_from should be mapped.
        """
        for ex in (ex_from, ex_to):
            if not issubclass(ex, Exception):
                raise ValueError(f"{ex} is not an instance of Exception")
        cls.EXCEPTION_MAP[ex_from] = ex_to

    def __init__(self, *expected, error_msg=None):
        """
        Args:
            *expected:
                The expected exceptions to transform into custom exceptions.
                These must be exception classes that are already in
                EXCEPTION_MAP.

            error_msg:
                An error message to prepend to the caught exception when
                instantiating the custom exception. It should provide context
                for the exception when it is displayed to the user.
        """
        expected = tuple(expected)
        for exception in expected:
            if exception not in self.EXCEPTION_MAP:
                raise ValueError(
                    f"{exception} is not currently mapped to any other exception"
                )
        self._expected = expected
        self.error_msg = error_msg

    def __enter__(self):
        return self._expected

    def __exit__(self, typ, value, traceback):
        if typ is not None:
            for exp_type in self._expected:
                if issubclass(typ, exp_type):
                    if self.error_msg:
                        arg = f"{self.error_msg}: {value}"
                    else:
                        arg = value
                    raise self.EXCEPTION_MAP[exp_type](arg) from value


def _declare_custom_exceptions():
    """
    Create custom subclasses for mapping common exceptions and add them to
    ExpectedExceptionContext exception map.
    """
    for std_exc in (KeyError, OSError, ValueError):
        name = std_exc.__name__
        custom_exc = type(f"Loader{name}", (std_exc,), {})
        custom_exc.__doc__ = f"Custom {name} exception."
        setattr(THIS_MODULE, custom_exc.__name__, custom_exc)
        ExpectedExceptionContext.EXCEPTION_MAP[std_exc] = custom_exc


_declare_custom_exceptions()
