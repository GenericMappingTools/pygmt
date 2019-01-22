"""
Low-level wrapper for the GMT C API.

The :class:`gmt.clib.Session` class wraps the GMT C shared library (``libgmt``)
with a pythonic interface.
Access to the C library is done through :py:mod:`ctypes`.

"""
from .session import Session
