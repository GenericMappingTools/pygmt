"""
ctypes wrappers for core functions from the C API
"""
import ctypes

from ..exceptions import GMTCLibNotFoundError, GMTCLibError
from .utils import clib_extension, check_status_code


def check_libgmt(libgmt):
    """
    Make sure that libgmt was loaded correctly.

    Checks if it defines some common required functions.

    Does nothing if everything is fine. Raises an exception if any of the
    functions are missing.

    Parameters
    ----------
    libgmt : ctypes.CDLL
        A shared library loaded using ctypes.

    Raises
    ------
    GMTCLibError

    """
    # Check if a few of the functions we need are in the library
    functions = ['Create_Session', 'Get_Enum', 'Call_Module',
                 'Destroy_Session']
    for func in functions:
        if not hasattr(libgmt, 'GMT_' + func):
            msg = ' '.join([
                "Error loading libgmt.",
                "Couldn't access function GMT_{}.".format(func),
            ])
            raise GMTCLibError(msg)


def load_libgmt(libname='libgmt'):
    """
    Find and load ``libgmt`` as a ctypes.CDLL.

    If not given the full path to the library, it must be in standard places or
    by discoverable by setting the environment variable ``LD_LIBRARY_PATH``.

    Parameters
    ----------
    libname : str
        The name of the GMT shared library **without the extension**. Can be a
        full path to the library or just the library name.

    Returns
    -------
    ctypes.CDLL object
        The loaded shared library.

    Raises
    ------
    GMTCLibNotFoundError
        If there was any problem loading the library (couldn't find it or
        couldn't access the functions).

    """
    try:
        libgmt = ctypes.CDLL('.'.join([libname, clib_extension()]))
        check_libgmt(libgmt)
    except OSError as err:
        msg = ' '.join([
            "Couldn't find the GMT shared library '{}'.".format(libname),
            "Have you tried setting the LD_LIBRARY_PATH environment variable?",
            "\nOriginal error message:",
            "\n\n    {}".format(str(err)),
        ])
        raise GMTCLibNotFoundError(msg)
    return libgmt


def create_session(session_name, libgmt):
    """
    Create the ``GMTAPI_CTRL`` struct required by the GMT C API functions.

    It is a C void pointer containing the current session information and
    cannot be accessed directly.

    Remember to terminate the current session using
    :func:`gmt.clib.LibGMT._destroy_session` before creating a new one.

    Parameters
    ----------
    session_name : str
        A name for this session. Doesn't really affect the outcome.
    libgmt : ctypes.CDLL
        The ``ctypes.CDLL`` instance for the libgmt shared library.

    Returns
    -------
    api_pointer : C void pointer (returned by ctypes as an integer)
        Used by GMT C API functions.

    """
    c_create_session = libgmt.GMT_Create_Session
    c_create_session.argtypes = [ctypes.c_char_p, ctypes.c_uint,
                                 ctypes.c_uint, ctypes.c_void_p]
    c_create_session.restype = ctypes.c_void_p
    # None is passed in place of the print function pointer. It becomes the
    # NULL pointer when passed to C, prompting the C API to use the default
    # print function.
    print_func = None
    padding = get_constant('GMT_PAD_DEFAULT', libgmt)
    session_type = get_constant('GMT_SESSION_EXTERNAL', libgmt)
    session = c_create_session(session_name.encode(), padding, session_type,
                               print_func)

    if session is None:
        raise GMTCLibError("Failed to create a GMT API void pointer.")

    return session


def destroy_session(session, libgmt):
    """
    Terminate and free the memory of a registered ``GMTAPI_CTRL`` session.

    The session is created and consumed by the C API modules and needs to
    be freed before creating a new. Otherwise, some of the configuration
    files might be left behind and can influence subsequent API calls.

    Parameters
    ----------
    session : C void pointer (returned by ctypes as an integer)
        The active session object produced by
        :func:`gmt.clib.core.create_session`.
    libgmt : ctypes.CDLL
        The ``ctypes.CDLL`` instance for the libgmt shared library.

    """
    c_destroy_session = libgmt.GMT_Destroy_Session
    c_destroy_session.argtypes = [ctypes.c_void_p]
    c_destroy_session.restype = ctypes.c_int

    status = c_destroy_session(session)
    check_status_code(status, 'GMT_Destroy_Session')


def get_constant(name, libgmt):
    """
    Get the value of a constant (C enum) from gmt_resources.h

    Used to set configuration values for other API calls. Wraps
    ``GMT_Get_Enum``.

    Parameters
    ----------
    name : str
        The name of the constant (e.g., ``"GMT_SESSION_EXTERNAL"``)
    libgmt : ctypes.CDLL
        The ``ctypes.CDLL`` instance for the libgmt shared library.

    Returns
    -------
    constant : int
        Integer value of the constant. Do not rely on this value because it
        might change.

    Raises
    ------
    GMTCLibError
        If the constant doesn't exist.

    """
    c_get_enum = libgmt.GMT_Get_Enum
    c_get_enum.argtypes = [ctypes.c_char_p]
    c_get_enum.restype = ctypes.c_int

    value = c_get_enum(name.encode())

    if value is None or value == -99999:
        raise GMTCLibError(
            "Constant '{}' doesn't exits in libgmt.".format(name))

    return value


def call_module(session, module, args, libgmt):
    """
    Call a GMT module with the given arguments.

    Makes a call to ``GMT_Call_Module`` from the C API using mode
    ``GMT_MODULE_CMD`` (arguments passed as a single string).

    Most interactions with the C API are done through this function.

    Parameters
    ----------
    session : C void pointer (returned by ctypes as an integer)
        The active session object produced by
        :func:`gmt.clib.core.create_session`.
    module : str
        Module name (``'pscoast'``, ``'psbasemap'``, etc).
    args : str
        String with the command line arguments that will be passed to the
        module (for example, ``'-R0/5/0/10 -JM'``).
    libgmt : ctypes.CDLL
        The ``ctypes.CDLL`` instance for the libgmt shared library.

    Raises
    ------
    GMTCLibError
        If the returned status code of the functions is non-zero.

    """
    c_call_module = libgmt.GMT_Call_Module
    c_call_module.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                              ctypes.c_int, ctypes.c_void_p]
    c_call_module.restype = ctypes.c_int

    mode = get_constant('GMT_MODULE_CMD', libgmt)
    status = c_call_module(session, module.encode(), mode,
                           args.encode())
    check_status_code(status, 'GMT_Call_Module')
