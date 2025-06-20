"""
Custom exception types used throughout the library.

All exceptions derive from GMTError.
"""

from collections.abc import Sequence
from typing import Any


class GMTError(Exception):
    """
    Base class for all GMT related errors.
    """


class GMTOSError(GMTError):
    """
    Unsupported operating system.
    """


class GMTCLibError(GMTError):
    """
    Error encountered when running a function from the GMT shared library.
    """


class GMTCLibNotFoundError(GMTCLibError):
    """
    Could not find the GMT shared library.
    """


class GMTCLibNoSessionError(GMTCLibError):
    """
    Tried to access GMT API without a currently open GMT session.
    """


class GMTInvalidInput(GMTError):  # noqa: N818
    """
    Raised when the input of a function/method is invalid.
    """


class GMTVersionError(GMTError):
    """
    Raised when an incompatible version of GMT is being used.
    """


class GMTImageComparisonFailure(AssertionError):  # noqa: N818
    """
    Raised when a comparison between two images fails.
    """


class GMTValueError(GMTError):
    """
    Raised when an invalid value is passed to a function/method.

    >>> raise GMTValueError("x", 1)
    Traceback (most recent call last):
    ...
    pygmt...GMTValueError: Invalid value for parameter 'x': 1.
    >>> raise GMTValueError("x", 1, choices=["a", "b", 1, 2])
    Traceback (most recent call last):
        ...
    pygmt...GMTValueError: ... 'x': 1. Expected one of: 'a', 'b', 1, 2.
    >>> raise GMTValueError("x", 1, choices=["a", 0, True, False, None])
    Traceback (most recent call last):
        ...
    pygmt...GMTValueError: ... 'x': 1. Expected one of: 'a', 0, True, False, None.
    """

    def __init__(self, name: str, value: Any, choices: Sequence[Any] | None = None):
        msg = f"Invalid value for parameter {name!r}: {value!r}."
        if choices is not None:
            msg += f" Expected one of: {', '.join(repr(c) for c in choices)}."
        super().__init__(msg)
