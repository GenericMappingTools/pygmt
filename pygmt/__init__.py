"""
PyGMT is a library for processing geospatial and geophysical data and making
publication-quality maps and figures. It provides a Pythonic interface for the Generic
Mapping Tools (GMT), a command-line program widely used across the Earth, Ocean, and
Planetary sciences and beyond. Besides making GMT more accessible to new users, PyGMT
aims to provide integration with the PyData ecosystem as well as support for rich
display in Jupyter notebooks.

Main Features
-------------
Here are just a few of the things that PyGMT does well:

  - Easy handling of individual types of data like Cartesian, geographic, or
    time-series data.
  - Processing of (geo)spatial data including gridding, filtering, and masking.
  - Plotting of a large spectrum of objects on figures including
    lines, vectors, polygons, and symbols (pre-defined and customized).
  - Generating publication-quality illustrations and making animations.
"""

import atexit as _atexit
import sys
from importlib.metadata import version

# Get semantic version through setuptools-scm
__version__ = f'v{version("pygmt")}'  # e.g. v0.1.2.dev3+g0ab3cd78
__commit__ = __version__.split("+g")[-1] if "+g" in __version__ else ""  # 0ab3cd78

# Import modules to make the high-level GMT Python API
from pygmt import datasets
from pygmt.accessors import GMTDataArrayAccessor
from pygmt.figure import Figure, set_display
from pygmt.io import load_dataarray
from pygmt.session_management import begin as _begin
from pygmt.session_management import end as _end
from pygmt.src import (
    binstats,
    blockmean,
    blockmedian,
    blockmode,
    config,
    dimfilter,
    filter1d,
    grd2cpt,
    grd2xyz,
    grdclip,
    grdcut,
    grdfill,
    grdfilter,
    grdgradient,
    grdhisteq,
    grdinfo,
    grdlandmask,
    grdproject,
    grdsample,
    grdtrack,
    grdvolume,
    info,
    makecpt,
    nearneighbor,
    project,
    select,
    sph2grd,
    sphdistance,
    sphinterpolate,
    surface,
    triangulate,
    which,
    x2sys_cross,
    x2sys_init,
    xyz2grd,
)

# Start our global modern mode session
_begin()
# Tell Python to run _end when shutting down
_atexit.register(_end)


def print_clib_info(file=sys.stdout):
    """
    Print information about the GMT shared library that we can find.

    Includes the GMT version, default values for parameters, the path to the
    ``libgmt`` shared library, and GMT directories.
    """
    from pygmt.clib import Session

    print("GMT library information:", file=file)
    with Session() as ses:
        lines = [f"  {key}: {ses.info[key]}" for key in sorted(ses.info)]
    print("\n".join(lines), file=file)


def show_versions(file=sys.stdout):
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

    import importlib
    import platform
    import shutil
    import subprocess

    from packaging.requirements import Requirement
    from packaging.version import Version

    def _get_clib_info() -> dict:
        """
        Return information about the GMT shared library.
        """
        from pygmt.clib import Session

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
        Get ghostscript version.
        """
        match sys.platform:
            case "linux" | "darwin":
                cmds = ["gs"]
            case os_name if os_name.startswith("freebsd"):
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

    def _check_ghostscript_version(gs_version: str) -> str | None:
        """
        Check if the Ghostscript version is compatible with GMT versions.
        """
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
                from pygmt.clib import __gmt_version__

                if Version(__gmt_version__) < Version("6.5.0"):
                    return (
                        f"GMT v{__gmt_version__} doesn't support Ghostscript "
                        "v{gs_version}. Please consider upgrading to GMT>=6.5.0 or "
                        "downgrading to Ghostscript v9.56."
                    )
        return None

    sys_info = {
        "python": sys.version.replace("\n", " "),
        "executable": sys.executable,
        "machine": platform.platform(),
    }
    deps = [Requirement(v).name for v in importlib.metadata.requires("pygmt")]
    gs_version = _get_ghostscript_version()

    lines = []
    lines.append("PyGMT information:")
    lines.append(f"  version: {__version__}")
    lines.append("System information:")
    lines.extend([f"  {key}: {val}" for key, val in sys_info.items()])
    lines.append("Dependency information:")
    lines.extend([f"  {modname}: {_get_module_version(modname)}" for modname in deps])
    lines.append(f"  ghostscript: {gs_version}")
    lines.append("GMT library information:")
    lines.extend([f"  {key}: {val}" for key, val in _get_clib_info().items()])

    if warnmsg := _check_ghostscript_version(gs_version):
        lines.append("WARNING:")
        lines.append(f"  {warnmsg}")

    print("\n".join(lines), file=file)
