"""
Utilities like finding and loading the GMT C library.
"""
import ctypes


def load_libgmt():
    """
    Find and load ``libgmt`` as a ctypes.CDLL.

    Currently only works for Linux (looks for ``libgmt.so``).

    Library path must be discoverable, either by being in standard places or by
    setting the environment variable ``LD_LIBRARY_PATH``.

    Returns
    -------
    ctypes.CDLL object
        The loaded shared library.

    """
    libgmt = ctypes.CDLL('libgmt.so')
    assert hasattr(libgmt, 'GMT_Create_Session'), \
        "Error loading libgmt. Can't access GMT_Create_Session."
    return libgmt
