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


class GMTCLibError(GMTError):
    """
    Error encountered when running a function from the GMT shared library.
    """
    pass


class GMTCLibNotFoundError(GMTCLibError):
    """
    Could not find the GMT shared library.
    """
    pass


class GMTCLibNoSessionError(GMTCLibError):
    """
    Tried to access GMT API without a currently open GMT session.
    """
    pass
