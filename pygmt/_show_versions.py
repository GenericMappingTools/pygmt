"""
Utility methods to print system information for debugging.

Adapted from :func:`rioxarray.show_versions` and :func:`pandas.show_versions`.
"""

import ctypes
import platform
import shutil
import subprocess
import sys
from importlib.metadata import PackageNotFoundError, requires, version
from typing import TextIO

from packaging.requirements import Requirement
from packaging.version import Version
from pygmt.clib import Session, __gmt_version__

# Get semantic version through setuptools-scm
__version__ = f"v{version('pygmt')}"  # e.g. v0.1.2.dev3+g0ab3cd78
__commit__ = __version__.split("+g")[-1] if "+g" in __version__ else ""  # 0ab3cd78


def _get_clib_info() -> dict[str, str]:
    """
    Get information about the GMT shared library.
    """
    with Session() as lib:
        return lib.info


def _get_module_version(modname: str) -> str | None:
    """
    Get version information of a Python module.
    """
    try:
        return version(modname)
    except PackageNotFoundError:
        return None


def _get_gdal_version() -> str | None:
    """
    Get GDAL version by calling the GDAL C API via ctypes.
    """
    match sys.platform:
        case name if name == "linux" or name.startswith("freebsd"):
            libname = "libgdal.so"
        case "darwin":
            libname = "libgdal.dylib"
        case "win32":
            libname = "gdal.dll"
        case _:
            return None

    try:
        lib = ctypes.CDLL(libname)
        lib.GDALVersionInfo.restype = ctypes.c_char_p
        return lib.GDALVersionInfo(b"RELEASE_NAME").decode("utf-8")  # e.g., 3.6.3
    except (OSError, AttributeError):
        return None


def _get_ghostscript_version() -> str | None:
    """
    Get Ghostscript version.
    """
    match sys.platform:
        case name if name in {"linux", "darwin"} or name.startswith("freebsd"):
            cmds = ["gs"]
        case "win32":
            cmds = ["gswin64c.exe", "gswin32c.exe"]
        case _:
            return None

    for gs_cmd in cmds:
        if (gsfullpath := shutil.which(gs_cmd)) is not None:
            return subprocess.check_output(
                [gsfullpath, "--version"], universal_newlines=True
            ).strip()
    return None


def _check_ghostscript_version(gs_version: str | None) -> str | None:
    """
    Check if the Ghostscript version is compatible with GMT versions.
    """
    if gs_version is None:
        return "Ghostscript is not detected. Your installation may be broken."

    match Version(gs_version):
        case v if v < Version("9.53"):
            return (
                f"Ghostscript v{gs_version} is too old and may have serious bugs. "
                "Please consider upgrading your Ghostscript."
            )
        case v if Version("10.00") <= v < Version("10.02"):
            return (
                f"Ghostscript v{gs_version} has known bugs. "
                "Please consider upgrading to version v10.02 or later."
            )
        case v if v >= Version("10.02") and Version(__gmt_version__) < Version("6.5.0"):
            return (
                f"GMT v{__gmt_version__} doesn't support Ghostscript v{gs_version}. "
                "Please consider upgrading to GMT>=6.5.0 or downgrading to Ghostscript "
                "v9.56."
            )
    return None


def show_versions(file: TextIO | None = sys.stdout) -> None:
    """
    Print various dependency versions which are useful when submitting bug reports.

    This includes information about:

    - PyGMT itself
    - System information (Python version, Operating System)
    - Core dependency versions (NumPy, pandas, Xarray, etc)
    - GDAL and Ghostscript versions
    - GMT library information

    It also warns users if the installed Ghostscript version has serious bugs or is
    incompatible with the installed GMT version.
    """
    sys_info = {
        "python": sys.version.replace("\n", " "),
        "executable": sys.executable,
        "machine": platform.platform(),
    }
    requirements = [Requirement(v).name for v in requires("pygmt")]  # type: ignore[union-attr]
    dep_info = {name: _get_module_version(name) for name in requirements}
    dep_info.update(
        {"gdal": _get_gdal_version(), "ghostscript": _get_ghostscript_version()}
    )

    lines = []
    lines.append("PyGMT information:")
    lines.append(f"  version: {__version__}")
    lines.append("System information:")
    lines.extend([f"  {key}: {val}" for key, val in sys_info.items()])
    lines.append("Dependency information:")
    lines.extend([f"  {key}: {val}" for key, val in dep_info.items()])
    lines.append("GMT library information:")
    lines.extend([f"  {key}: {val}" for key, val in _get_clib_info().items()])

    if warnmsg := _check_ghostscript_version(dep_info["ghostscript"]):
        lines.append("WARNING:")
        lines.append(f"  {warnmsg}")

    print("\n".join(lines), file=file)
