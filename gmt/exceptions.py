"""
Our custom exceptions
"""


class GMTError(Exception):
    """
    Base class for all GMT related errors.
    """
    pass


class GMTOSError(GMTError):
    """
    Unsupported operating system.
    """
    pass


class GMTCLibNotFoundError(GMTError):
    """
    Could not find the GMT shared library.
    """
    pass


class GMTCLibError(GMTError):
    """
    Error encountered when running a function from the GMT shared library.
    """
    pass
