"""
Utility functions to load libgmt as ctypes.CDLL.

The path to the shared library can be found automatically by ctypes or set through the
GMT_LIBRARY_PATH environment variable.
"""

import ctypes
import os
import shutil
import subprocess as sp
import sys
from collections.abc import Iterator, Mapping
from ctypes.util import find_library
from pathlib import Path

from pygmt.exceptions import GMTCLibError, GMTCLibNotFoundError, GMTOSError


def load_libgmt(lib_fullnames: Iterator[str] | None = None) -> ctypes.CDLL:
    """
    Find and load ``libgmt`` as a :py:class:`ctypes.CDLL`.

    Will look for the GMT shared library in the directories determined by
    ``clib_full_names()``.

    Parameters
    ----------
    lib_fullnames
        List of possible full names of GMT's shared library. If ``None``, will default
        to ``clib_full_names()``.

    Returns
    -------
    libgmt
        The loaded shared library.

    Raises
    ------
    GMTCLibNotFoundError
        If there was any problem loading the library (couldn't find it or couldn't
        access the functions).
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


def get_gmt_version(libgmt: ctypes.CDLL) -> str:
    """
    Get the GMT version string of the GMT shared library.

    Parameters
    ----------
    libgmt
        The GMT shared library.

    Returns
    -------
    The GMT version string in *major.minor.patch* format.
    """
    func = libgmt.GMT_Get_Version
    func.argtypes = (
        ctypes.c_void_p,  # Unused parameter, so it can be None.
        ctypes.POINTER(ctypes.c_uint),  # major
        ctypes.POINTER(ctypes.c_uint),  # minor
        ctypes.POINTER(ctypes.c_uint),  # patch
    )
    # The function return value is the current library version as a float, e.g., 6.5.
    func.restype = ctypes.c_float
    major, minor, patch = ctypes.c_uint(0), ctypes.c_uint(0), ctypes.c_uint(0)
    func(None, major, minor, patch)
    return f"{major.value}.{minor.value}.{patch.value}"


def clib_names(os_name: str) -> list[str]:
    """
    Return the name(s) of GMT's shared library for the current operating system.

    Parameters
    ----------
    os_name
        The operating system name as given by ``sys.platform``.

    Returns
    -------
    libnames
        List of possible names of GMT's shared library.

    Raises
    ------
    GMTOSError
        If the operating system is not supported yet.
    """
    match os_name:
        case name if name == "linux" or name.startswith("freebsd"):  # Linux or FreeBSD
            libnames = ["libgmt.so"]
        case "darwin":  # macOS
            libnames = ["libgmt.dylib"]
        case "win32":  # Windows
            libnames = ["gmt.dll", "gmt_w64.dll", "gmt_w32.dll"]
        case _:
            raise GMTOSError(f"Operating system '{os_name}' is not supported.")
    return libnames


def clib_full_names(env: Mapping | None = None) -> Iterator[str]:
    """
    Return full path(s) of GMT shared library for the current operating system.

    The GMT shared library is searched for in following ways, sorted by priority:

    1. Path defined by environmental variable GMT_LIBRARY_PATH
    2. Path returned by command "gmt --show-library"
    3. Path defined by environmental variable PATH (Windows only)
    4. System default search path

    Parameters
    ----------
    env
        A dictionary containing the environment variables. If ``None``, will default to
        ``os.environ``.

    Yields
    ------
    lib_fullnames
        List of possible full names of GMT shared library.
    """
    if env is None:
        env = os.environ

    libnames = clib_names(os_name=sys.platform)  # e.g. libgmt.so, libgmt.dylib, gmt.dll

    # Search for the library in different ways, sorted by priority.
    # 1. Search for the library in GMT_LIBRARY_PATH if defined.
    if libpath := env.get("GMT_LIBRARY_PATH"):  # e.g. $HOME/miniconda/envs/pygmt/lib
        for libname in libnames:
            libfullpath = Path(libpath) / libname
            if libfullpath.exists():
                yield str(libfullpath)

    # 2. Search for the library returned by command "gmt --show-library".
    #    Use `str(Path(realpath))` to avoid mixture of separators "\\" and "/".
    if gmtbin := shutil.which("gmt"):
        try:
            libfullpath = Path(
                sp.check_output([gmtbin, "--show-library"], encoding="utf-8").rstrip()
            )
            if libfullpath.exists():
                yield str(libfullpath)
        except sp.CalledProcessError:  # the 'gmt' executable is broken
            pass

    # 3. Search for DLLs in PATH by calling find_library() (Windows only)
    if sys.platform == "win32":
        for libname in libnames:
            if libfullpath := find_library(libname):
                yield libfullpath

    # 4. Search for library names in the system default path
    for libname in libnames:
        yield libname


def check_libgmt(libgmt: ctypes.CDLL):
    """
    Make sure the GMT shared library was loaded correctly.

    Checks if the GMT shared library defines a few of the required functions. Does
    nothing if everything is fine. Raises an exception if any of the functions are
    missing.

    Parameters
    ----------
    libgmt
        A shared library loaded using ctypes.

    Raises
    ------
    GMTCLibError
    """
    for func in ["Create_Session", "Get_Enum", "Call_Module", "Destroy_Session"]:
        if not hasattr(libgmt, "GMT_" + func):
            msg = (
                f"Error loading '{libgmt._name}'. Couldn't access function GMT_{func}. "
                "Ensure that you have installed an up-to-date GMT version 6 library and "
                "set the environment variable 'GMT_LIBRARY_PATH' to the directory of "
                "the GMT 6 library."
            )
            raise GMTCLibError(msg)
