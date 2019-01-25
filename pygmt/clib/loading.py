"""
Utility functions to load libgmt as ctypes.CDLL.

The path to the shared library can be found automatically by ctypes or set through the
GMT_LIBRARY_PATH environment variable.
"""
import os
import sys
import ctypes

from ..exceptions import GMTOSError, GMTCLibError, GMTCLibNotFoundError


def load_libgmt(env=None):
    """
    Find and load ``libgmt`` as a :py:class:`ctypes.CDLL`.

    By default, will look for the shared library in the directory specified by
    the environment variable ``GMT_LIBRARY_PATH``. If it's not set, will let
    ctypes try to find the library.

    Parameters
    ----------
    env : dict or None
        A dictionary containing the environment variables. If ``None``, will
        default to ``os.environ``.

    Returns
    -------
    :py:class:`ctypes.CDLL` object
        The loaded shared library.

    Raises
    ------
    GMTCLibNotFoundError
        If there was any problem loading the library (couldn't find it or
        couldn't access the functions).

    """
    libpath = get_clib_path(env)
    try:
        libgmt = ctypes.CDLL(libpath)
        check_libgmt(libgmt)
    except OSError as err:
        msg = "\n".join(
            [
                "Error loading the GMT shared library '{}':".format(libpath),
                "{}".format(str(err)),
            ]
        )
        raise GMTCLibNotFoundError(msg)
    return libgmt


def get_clib_path(env):
    """
    Get the path to the libgmt shared library.

    Determine the file name and extension and append to the path set by
    ``GMT_LIBRARY_PATH``, if any.

    Parameters
    ----------
    env : dict or None
        A dictionary containing the environment variables. If ``None``, will
        default to ``os.environ``.

    Returns
    -------
    libpath : str
        The path to the libgmt shared library.

    """
    libname = ".".join(["libgmt", clib_extension()])
    if env is None:
        env = os.environ
    if "GMT_LIBRARY_PATH" in env:
        libpath = os.path.join(env["GMT_LIBRARY_PATH"], libname)
    else:
        libpath = libname
    return libpath


def clib_extension(os_name=None):
    """
    Return the extension for the shared library for the current OS.

    .. warning::

        Currently only works for macOS and Linux.

    Returns
    -------
    os_name : str or None
        The operating system name as given by ``sys.platform``
        (the default if None).

    Returns
    -------
    ext : str
        The extension ('.so', '.dylib', etc).

    """
    if os_name is None:
        os_name = sys.platform
    # Set the shared library extension in a platform independent way
    if os_name.startswith("linux"):
        lib_ext = "so"
    elif os_name == "darwin":
        # Darwin is macOS
        lib_ext = "dylib"
    else:
        raise GMTOSError('Operating system "{}" not supported.'.format(sys.platform))
    return lib_ext


def check_libgmt(libgmt):
    """
    Make sure that libgmt was loaded correctly.

    Checks if it defines some common required functions.

    Does nothing if everything is fine. Raises an exception if any of the
    functions are missing.

    Parameters
    ----------
    libgmt : :py:class:`ctypes.CDLL`
        A shared library loaded using ctypes.

    Raises
    ------
    GMTCLibError

    """
    # Check if a few of the functions we need are in the library
    functions = ["Create_Session", "Get_Enum", "Call_Module", "Destroy_Session"]
    for func in functions:
        if not hasattr(libgmt, "GMT_" + func):
            msg = " ".join(
                [
                    "Error loading libgmt.",
                    "Couldn't access function GMT_{}.".format(func),
                ]
            )
            raise GMTCLibError(msg)
