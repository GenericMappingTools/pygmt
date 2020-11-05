# pylint: disable=missing-docstring
#
# The main API for PyGMT.
#
# All of PyGMT is operated on a "modern mode session" (new to GMT6). When you
# import the pygmt library, a new session will be started automatically. The
# session will be closed when the current Python process terminates. Thus, the
# Python API does not expose the `gmt begin` and `gmt end` commands.

import atexit as _atexit

from ._version import get_versions as _get_versions

# Import modules to make the high-level GMT Python API
from .session_management import begin as _begin, end as _end
from .figure import Figure
from .filtering import blockmedian
from .gridding import surface
from .sampling import grdtrack
from .mathops import makecpt
from .modules import GMTDataArrayAccessor, config, info, grdinfo, which
from .gridops import grdcut, grdfilter
from .x2sys import x2sys_init, x2sys_cross
from . import datasets


# Get the version number through versioneer
__version__ = _get_versions()["version"]
__commit__ = _get_versions()["full-revisionid"]

# Start our global modern mode session
_begin()
# Tell Python to run _end when shutting down
_atexit.register(_end)


def print_clib_info():
    """
    Print information about the GMT shared library that we can find.

    Includes the GMT version, default values for parameters, the path to the
    ``libgmt`` shared library, and GMT directories.
    """
    from .clib import Session

    lines = ["GMT library information:"]
    with Session() as ses:
        for key in sorted(ses.info):
            lines.append("  {}: {}".format(key, ses.info[key]))
    print("\n".join(lines))


def show_versions():
    """
    Prints various dependency versions useful when submitting bug reports. This
    includes information about:

    - PyGMT itself
    - System information (Python version, Operating System)
    - Core dependency versions (Numpy, Pandas, Xarray, etc)
    - GMT library information
    """

    import sys
    import platform
    import importlib
    import subprocess

    def _get_module_version(modname):
        """Get version information of a Python module."""
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

    def _get_ghostscript_version():
        """Get ghostscript version."""
        os_name = sys.platform
        if os_name.startswith("linux") or os_name == "darwin":
            cmds = ["gs"]
        elif os_name == "win32":
            cmds = ["gswin64c.exe", "gswin32c.exe"]
        else:
            return None

        for gs_cmd in cmds:
            try:
                version = subprocess.check_output(
                    [gs_cmd, "--version"], universal_newlines=True
                ).strip()
                return version
            except FileNotFoundError:
                continue
        return None

    def _get_gmt_version():
        """Get GMT version."""
        try:
            version = subprocess.check_output(
                ["gmt", "--version"], universal_newlines=True
            ).strip()
            return version
        except FileNotFoundError:
            return None

    sys_info = {
        "python": sys.version.replace("\n", " "),
        "executable": sys.executable,
        "machine": platform.platform(),
    }

    deps = ["numpy", "pandas", "xarray", "netCDF4", "packaging"]

    print("PyGMT information:")
    print(f"  version: {__version__}")

    print("System information:")
    for key, val in sys_info.items():
        print(f"  {key}: {val}")

    print("Dependency information:")
    for modname in deps:
        print(f"  {modname}: {_get_module_version(modname)}")
    print(f"  ghostscript: {_get_ghostscript_version()}")
    print(f"  gmt: {_get_gmt_version()}")

    print_clib_info()


def test(doctest=True, verbose=True, coverage=False, figures=True):
    """
    Run the test suite.

    Uses `pytest <http://pytest.org/>`__ to discover and run the tests. If you
    haven't already, you can install it with `conda
    <http://conda.pydata.org/>`__ or `pip <https://pip.pypa.io/en/stable/>`__.

    Parameters
    ----------

    doctest : bool
        If ``True``, will run the doctests as well (code examples that start
        with a ``>>>`` in the docs).
    verbose : bool
        If ``True``, will print extra information during the test run.
    coverage : bool
        If ``True``, will run test coverage analysis on the code as well.
        Requires ``pytest-cov``.
    figures : bool
        If ``True``, will test generated figures against saved baseline
        figures.  Requires ``pytest-mpl`` and ``matplotlib``.

    Raises
    ------

    AssertionError
        If pytest returns a non-zero error code indicating that some tests have
        failed.

    """
    import pytest

    show_versions()

    package = __name__

    args = []
    if verbose:
        args.append("-vv")
    if coverage:
        args.append("--cov={}".format(package))
        args.append("--cov-report=term-missing")
    if doctest:
        args.append("--doctest-modules")
    if figures:
        args.append("--mpl")
    args.append("--pyargs")
    args.append(package)
    status = pytest.main(args)
    assert status == 0, "Some tests have failed."
