"""
Utility functions to load libgmt as ctypes.CDLL.

The path to the shared library can be found automatically by ctypes or set
through the GMT_LIBRARY_PATH environment variable.
"""
import os
import sys
import ctypes
from ctypes.util import find_library

from ..exceptions import GMTOSError, GMTCLibError, GMTCLibNotFoundError


def load_libgmt():
    """
    Find and load ``libgmt`` as a :py:class:`ctypes.CDLL`.

    By default, will look for the shared library in the directory specified by
    the environment variable ``GMT_LIBRARY_PATH``. If it's not set, will let
    ctypes try to find the library.

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
    lib_fullnames = clib_full_names()
    error = True
    for libname in lib_fullnames:
        try:
            libgmt = ctypes.CDLL(libname)
            check_libgmt(libgmt)
            error = False
            break
        except OSError as err:
            error = err
    if error:
        raise GMTCLibNotFoundError(
            "Error loading the GMT shared library '{}':".format(
                ", ".join(lib_fullnames)
            )
        )
    return libgmt


def clib_names(os_name):
    """
    Return the name of GMT's shared library for the current OS.

    Parameters
    ----------
    os_name : str
        The operating system name as given by ``sys.platform``.

    Returns
    -------
    libnames : list of str
        List of possible names of GMT's shared library.

    """
    if os_name.startswith("linux"):
        libnames = ["libgmt.so"]
    elif os_name == "darwin":
        # Darwin is macOS
        libnames = ["libgmt.dylib"]
    elif os_name == "win32":
        libnames = ["gmt.dll", "gmt_w64.dll", "gmt_w32.dll"]
    else:
        raise GMTOSError('Operating system "{}" not supported.'.format(sys.platform))
    return libnames


def clib_full_names(env=None):
    """
    Return the full path of GMT's shared library for the current OS.

    Parameters
    ----------
    env : dict or None
        A dictionary containing the environment variables. If ``None``, will
        default to ``os.environ``.

    Returns
    -------
    lib_fullnames: list of str
        List of possible full names of GMT's shared library.

    """
    if env is None:
        env = os.environ
    libnames = clib_names(os_name=sys.platform)  # e.g. libgmt.so, libgmt.dylib, gmt.dll
    libpath = env.get("GMT_LIBRARY_PATH", "")  # e.g. $HOME/miniconda/envs/pygmt/lib

    lib_fullnames = [os.path.join(libpath, libname) for libname in libnames]
    # Search for DLLs in PATH if GMT_LIBRARY_PATH is not defined [Windows only]
    if not libpath and sys.platform == "win32":
        for libname in libnames:
            libfullpath = find_library(libname)
            if libfullpath:
                lib_fullnames.append(libfullpath)
    return lib_fullnames


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
