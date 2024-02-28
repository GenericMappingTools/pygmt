"""
Functions for GMT library version.
"""

import ctypes as ctp

from packaging.version import Version


def get_gmt_version(libgmt: ctp.CDLL) -> Version:
    """
    Get the GMT version from shared library.

    Parameters
    ----------
    libgmt
        The GMT shared library.

    Returns
    -------
    version
        The GMT version.
    """
    func = libgmt.GMT_Get_Version
    func.argtypes = (
        ctp.c_void_p,
        ctp.POINTER(ctp.c_uint),
        ctp.POINTER(ctp.c_uint),
        ctp.POINTER(ctp.c_uint),
    )
    func.restype = ctp.c_float
    major, minor, patch = ctp.c_uint(999), ctp.c_uint(999), ctp.c_uint(999)
    func(None, major, minor, patch)
    return Version(f"{major.value}.{minor.value}.{patch.value}")
