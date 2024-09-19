"""
Test multiprocessing support.
"""

import multiprocessing as mp
from importlib import reload
from pathlib import Path

from pygmt import Figure


def _func(figname):
    """
    A wrapper function for testing multiprocessing support.
    """
    fig = Figure()
    fig.basemap(region=[10, 70, -3, 8], projection="X8c/6c", frame="afg")
    fig.savefig(figname)


def test_multiprocessing():
    """
    Make sure that multiprocessing is supported if pygmt is re-imported.
    """
    prefix = "test_session_multiprocessing"
    with mp.Pool(2) as p:
        p.map(_func, [f"{prefix}-1.png", f"{prefix}-2.png"])
    Path(f"{prefix}-1.png").unlink()
    Path(f"{prefix}-2.png").unlink()


def _func_reload(figname):
    """
    A wrapper for running PyGMT scripts with multiprocessing.

    Before the official multiprocessing support in PyGMT, we have to reload the
    PyGMT library. Workaround from
    https://github.com/GenericMappingTools/pygmt/issues/217#issuecomment-754774875.

    This test makes sure that the old workaround still works.
    """
    import pygmt

    reload(pygmt)
    fig = pygmt.Figure()
    fig.basemap(region=[10, 70, -3, 8], projection="X8c/6c", frame="afg")
    fig.savefig(figname)


def test_multiprocessing_reload():
    """
    Make sure that multiprocessing is supported if pygmt is re-imported.
    """

    prefix = "test_session_multiprocessing"
    with mp.Pool(2) as p:
        p.map(_func_reload, [f"{prefix}-1.png", f"{prefix}-2.png"])
    Path(f"{prefix}-1.png").unlink()
    Path(f"{prefix}-2.png").unlink()
