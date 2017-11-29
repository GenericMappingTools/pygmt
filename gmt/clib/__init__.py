"""
Low-level wrapper for the GMT C API.

The :class:`gmt.clib.LibGMT` class wraps the GMT C shared library (``libgmt``)
with a pythonic interface.
Access to the C library is done through
`ctypes <https://docs.python.org/3/library/ctypes.html>`__.

"""
from .core import LibGMT
