# pylint: disable=missing-docstring
#
# Custom exception types used throughout the library. All exceptions derive
# from GMTError.


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


class GMTInvalidInput(GMTError):
    """
    Raised when the input of a function/method is invalid.
    """


class GMTVersionError(GMTError):
    """
    Raised when an incompatible version of GMT is being used.
    """


class GMTImageComparisonFailure(AssertionError):
    """
    Raised when a comparison between two images fails.
    """
