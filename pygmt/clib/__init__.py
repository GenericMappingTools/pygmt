"""
Low-level wrapper for the GMT C API.

The pygmt.clib.Session class wraps the GMT C shared library (libgmt) with a Pythonic
interface. Access to the C library is done through ctypes.
"""
from packaging.version import Version
from pygmt.clib.session import Session
from pygmt.exceptions import GMTVersionError

with Session() as lib:
    __gmt_version__ = lib.info["version"]
    if Version(__gmt_version__) < Version(lib.required_version):
        raise GMTVersionError(
            f"Using an incompatible GMT version {__gmt_version__}. "
            f"Must be equal or newer than {lib.required_version}."
        )
