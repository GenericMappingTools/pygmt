"""
Low-level wrapper for the GMT C API.

The pygmt.clib.Session class wraps the GMT C shared library (libgmt) with a Pythonic
interface. Access to the C library is done through ctypes.
"""

from packaging.version import Version
from pygmt.clib.session import Session, __gmt_version__
from pygmt.exceptions import GMTVersionError

required_gmt_version = "6.3.0"

# Check if the GMT version is older than the required version.
if Version(__gmt_version__) < Version(required_gmt_version):
    msg = (
        f"Using an incompatible GMT version {__gmt_version__}. "
        f"Must be equal or newer than {required_gmt_version}."
    )
    raise GMTVersionError(msg)
