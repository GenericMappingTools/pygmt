"""
Low-level wrapper for the GMT C API.

The pygmt.clib.Session class wraps the GMT C shared library (libgmt) with a Pythonic
interface. Access to the C library is done through ctypes.
"""

from pygmt.clib.session import Session

with Session() as lib:
    __gmt_version__ = lib.info["version"]
