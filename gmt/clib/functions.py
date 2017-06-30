"""
ctypes wrappers for functions from the C API
"""
import ctypes


def create_session():
    """
    Create an ``API`` struct that contains the current session information.

    This is a C void pointer and cannot be accessed in Python. It is required
    by the GMT C API functions.

    Return
    ------
    api_pointer : C void pointer
        Used by GMT C API functions.

    """
    pass
