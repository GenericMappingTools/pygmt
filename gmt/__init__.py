"""
GMT Python interface
"""
from ._version import get_versions

# Import modules to make the high-level GMT Python API
from .ps_modules import pscoast
from .session_management import figure, GMTSession


# Get the version number through versioneer
__version__ = get_versions()['version']
# Delete the function so that it doesn't appear in the public API
del get_versions

# Start our global modern mode session. It calls "gmt.begin" when started and
# "gmt.end" when deleted.
_GLOBAL_SESSION = GMTSession()
# Delete the class so that it doesn't appear in the public API
del GMTSession


def test(doctest=True, verbose=True, coverage=False, figures=True):
    """
    Run the test suite.

    Uses `py.test <http://pytest.org/>`__ to discover and run the tests. If you
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
    args = []
    if verbose:
        args.append('-vv')
    if coverage:
        args.append('--cov=gmt')
        args.append('--cov-report=term-missing')
    if doctest:
        args.append('--doctest-modules')
    if figures:
        args.append('--mpl')
    args.append('--pyargs')
    args.append('gmt')
    status = pytest.main(args)
    assert status == 0, "Some tests have failed."
