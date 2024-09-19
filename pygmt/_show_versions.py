"""
Utility methods to print system info for debugging.

Adapted from :func:`rioxarray.show_versions` and :func:`pandas.show_versions`.
"""

import importlib
import platform
import shutil
import subprocess
import sys
from importlib.metadata import version
from typing import TextIO

from packaging.requirements import Requirement
from packaging.version import Version
from pygmt.clib import Session, __gmt_version__

# Get semantic version through setuptools-scm
__version__ = f'v{version("pygmt")}'  # e.g. v0.1.2.dev3+g0ab3cd78
__commit__ = __version__.split("+g")[-1] if "+g" in __version__ else ""  # 0ab3cd78


def _get_clib_info() -> dict[str, str]:
    """
    Get information about the GMT shared library.
    """
    with Session() as ses:
        return ses.info


def _get_module_version(modname: str) -> str | None:
    """
    Get version information of a Python module.
    """
    try:
        if modname in sys.modules:
            module = sys.modules[modname]
        else:
            module = importlib.import_module(modname)

        try:
            return module.__version__
        except AttributeError:
            return module.version
    except ImportError:
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
        case v if v >= Version("10.02"):
            if Version(__gmt_version__) < Version("6.5.0"):
                return (
                    f"GMT v{__gmt_version__} doesn't support Ghostscript "
                    f"v{gs_version}. Please consider upgrading to GMT>=6.5.0 or "
                    "downgrading to Ghostscript v9.56."
                )
    return None


def show_versions(file: TextIO | None = sys.stdout):
    """
    Print various dependency versions which are useful when submitting bug reports.

    This includes information about:

    - PyGMT itself
    - System information (Python version, Operating System)
    - Core dependency versions (NumPy, Pandas, Xarray, etc)
    - GMT library information

    It also warns users if the installed Ghostscript version has serious bugs or is
    incompatible with the installed GMT version.
    """

    sys_info = {
        "python": sys.version.replace("\n", " "),
        "executable": sys.executable,
        "machine": platform.platform(),
    }
    dep_info = {
        Requirement(v).name: _get_module_version(Requirement(v).name)
        for v in importlib.metadata.requires("pygmt")  # type: ignore[union-attr]
    }
    dep_info.update(
        {
            "gdal": _get_module_version("osgeo.gdal"),
            "ghostscript": _get_ghostscript_version(),
        }
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
