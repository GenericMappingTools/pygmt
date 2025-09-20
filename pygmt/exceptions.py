"""
Custom exception types used throughout the library.

All exceptions derive from GMTError.
"""

from collections.abc import Iterable
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


class GMTValueError(GMTError, ValueError):
    """
    Raised when an invalid value is passed to a function/method.

    Parameters
    ----------
    value
        The invalid value.
    description
        The description of the value.
    choices
        The valid choices for the value.
    reason
        The detailed reason why the value is invalid.

    Examples
    --------
    >>> raise GMTValueError("invalid")
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTValueError: Invalid value: 'invalid'.
    >>> raise GMTValueError("invalid", description="constant name")
    Traceback (most recent call last):
    ...
    pygmt.exceptions.GMTValueError: Invalid constant name: 'invalid'.
    >>> raise GMTValueError("invalid", choices=["a", "b", 1, 2])
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTValueError: Invalid value: 'invalid'. Expected one of: 'a', 'b', 1, 2.
    >>> raise GMTValueError("invalid", choices=["a", 0, True, False, None])
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTValueError: Invalid value: 'invalid'. Expected one of: 'a', 0, True, False, None.

    >>> from pygmt.enums import GridType
    >>> raise GMTValueError("invalid", choices=GridType)
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTValueError: Invalid value: 'invalid'. Expected one of: <GridType.CARTESIAN: 0>, <GridType.GEOGRAPHIC: 1>.
    >>> raise GMTValueError("invalid", reason="Explain why it's invalid.")
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTValueError: Invalid value: 'invalid'. Explain why it's invalid.
    """  # noqa: W505

    def __init__(
        self,
        value: Any,
        /,
        description: str = "value",
        choices: Iterable[Any] | None = None,
        reason: str | None = None,
    ):
        msg = f"Invalid {description}: {value!r}."
        if choices:
            msg += f" Expected one of: {', '.join(repr(c) for c in choices)}."
        if reason:
            msg += f" {reason}"
        super().__init__(msg)


class GMTTypeError(GMTError, TypeError):
    """
    Raised when an invalid type is passed to a function/method.

    This exception is used to indicate that the type of an argument does not match
    the expected type.
    """

    def __init__(self, dtype: object, /, reason: str | None = None):
        msg = f"Unrecognized data type: {dtype!r}."
        if reason:
            msg += f" {reason}"
        super().__init__(msg)
