"""
Test multiprocessing support.
"""

import multiprocessing as mp
from importlib import reload
from pathlib import Path

import numpy.testing as npt
import pygmt


def _func(figname):
    """
    A wrapper function for testing multiprocessing support.
    """
    fig = pygmt.Figure()
    fig.basemap(region=[10, 70, -3, 8], projection="X8c/6c", frame="afg")
    fig.savefig(figname)


def test_multiprocessing():
    """
    Test multiprocessing support for plotting figures.
    """
    prefix = "test_session_multiprocessing"
    with mp.Pool(2) as p:
        p.map(_func, [f"{prefix}-1.png", f"{prefix}-2.png"])
    Path(f"{prefix}-1.png").unlink()
    Path(f"{prefix}-2.png").unlink()


def _func_datacut(dataset):
    """
    A wrapper function for testing multiprocessing support.
    """
    xrgrid = pygmt.grdcut(dataset, region=[-10, 10, -5, 5])
    return xrgrid


def test_multiprocessing_data_processing():
    """
    Test multiprocessing support for data processing.
    """
    with mp.Pool(2) as p:
        grids = p.map(_func_datacut, ["@earth_relief_01d_g", "@moon_relief_01d_g"])
    assert len(grids) == 2
    # The Earth relief dataset
    assert grids[0].shape == (11, 21)
    npt.assert_allclose(grids[0].min(), -5118.0, atol=0.5)
    npt.assert_allclose(grids[0].max(), 680.5, atol=0.5)
    # The Moon relief dataset
    assert grids[1].shape == (11, 21)
    npt.assert_allclose(grids[1].min(), -1122.0, atol=0.5)
    npt.assert_allclose(grids[1].max(), 943.0, atol=0.5)


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
