"""
Utility functions to load libgmt as ctypes.CDLL.

The path to the shared library can be found automatically by ctypes or set
through the GMT_LIBRARY_PATH environment variable.
"""
import ctypes
import os
import subprocess as sp
import sys
from ctypes.util import find_library
from pathlib import Path

from pygmt.exceptions import GMTCLibError, GMTCLibNotFoundError, GMTOSError


def load_libgmt(lib_fullnames=None):
    """
    Find and load ``libgmt`` as a :py:class:`ctypes.CDLL`.

    Will look for the GMT shared library in the directories determined by
    clib_full_names().

    Parameters
    ----------
    lib_fullnames : list of str or None
        List of possible full names of GMT's shared library. If ``None``, will
        default to ``clib_full_names()``.

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
    if lib_fullnames is None:
        lib_fullnames = clib_full_names()

    error = True
    error_msg = []
    failing_libs = []
    for libname in lib_fullnames:
        try:
            if libname not in failing_libs:  # skip the lib if it's known to fail
                libgmt = ctypes.CDLL(libname)
                check_libgmt(libgmt)
                error = False
                break
        except (OSError, GMTCLibError) as err:
            error_msg.append(f"Error loading GMT shared library at '{libname}'.\n{err}")
            failing_libs.append(libname)

    if error:
        raise GMTCLibNotFoundError("\n".join(error_msg))

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
    if os_name.startswith(("linux", "freebsd")):
        libnames = ["libgmt.so"]
    elif os_name == "darwin":  # Darwin is macOS
        libnames = ["libgmt.dylib"]
    elif os_name == "win32":
        libnames = ["gmt.dll", "gmt_w64.dll", "gmt_w32.dll"]
    else:
        raise GMTOSError(f"Operating system '{os_name}' not supported.")
    return libnames


def clib_full_names(env=None):
    """
    Return the full path of GMT's shared library for the current OS.

    Parameters
    ----------
    env : dict or None
        A dictionary containing the environment variables. If ``None``, will
        default to ``os.environ``.

    Yields
    ------
    lib_fullnames: list of str
        List of possible full names of GMT's shared library.
    """
    if env is None:
        env = os.environ

    libnames = clib_names(os_name=sys.platform)  # e.g. libgmt.so, libgmt.dylib, gmt.dll

    # Search for the library in different ways, sorted by priority.
    # 1. Search for the library in GMT_LIBRARY_PATH if defined.
    libpath = env.get("GMT_LIBRARY_PATH", "")  # e.g. $HOME/miniconda/envs/pygmt/lib
    if libpath:
        for libname in libnames:
            libfullpath = Path(libpath) / libname
            if libfullpath.exists():
                yield str(libfullpath)

    # 2. Search for the library returned by command "gmt --show-library"
    #    Use `str(Path(realpath))` to avoid mixture of separators "\\" and "/"
    try:
        libfullpath = Path(
            sp.check_output(["gmt", "--show-library"], encoding="utf-8").rstrip("\n")
        )
        assert libfullpath.exists()
        yield str(libfullpath)
    except (FileNotFoundError, AssertionError, sp.CalledProcessError):
        # the 'gmt' executable  is not found
        # the gmt library is not found
        # the 'gmt' executable is broken
        pass

    # 3. Search for DLLs in PATH by calling find_library() (Windows only)
    if sys.platform == "win32":
        for libname in libnames:
            libfullpath = find_library(libname)
            if libfullpath:
                yield libfullpath

    # 4. Search for library names in the system default path
    for libname in libnames:
        yield libname


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
            # pylint: disable=protected-access
            msg = (
                f"Error loading '{libgmt._name}'. Couldn't access function GMT_{func}. "
                "Ensure that you have installed an up-to-date GMT version 6 library. "
                "Please set the environment variable 'GMT_LIBRARY_PATH' to the "
                "directory of the GMT 6 library."
            )
            raise GMTCLibError(msg)
