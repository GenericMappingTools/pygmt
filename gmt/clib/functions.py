"""
ctypes wrappers for functions from the C API
"""
import ctypes

from .utils import load_libgmt
from .constants import GMT_SESSION_NAME, GMT_PAD_DEFAULT, GMT_SESSION_EXTERNAL


def create_session():
    """
    Create the ``GMTAPI_CTRL`` struct required by the GMT C API functions.

    It is a C void pointer containing the current session information and
    cannot be accessed directly.

    Returns
    -------
    api_pointer : C void pointer (returned by ctypes as an integer)
        Used by GMT C API functions.

    """
    libgmt = load_libgmt()
    c_create_session = libgmt.GMT_Create_Session
    c_create_session.argtypes = [ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint,
                                 ctypes.c_void_p]
    c_create_session.restype = ctypes.c_void_p
    # None is passed in place of the print function pointer. It becomes the
    # NULL pointer when passed to C, prompting the C API to use the default
    # print function.
    session = c_create_session(GMT_SESSION_NAME, GMT_PAD_DEFAULT,
                               GMT_SESSION_EXTERNAL, None)
    assert session is not None, \
        "Failed creating GMT API pointer using create_session."
    return session
