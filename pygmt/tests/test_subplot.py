"""
Tests subplot.
"""
import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers.testing import check_figures_equal


@check_figures_equal()
def test_subplot_basic_frame():
    """
    Create a subplot figure with 1 vertical row and 2 horizontal columns, and
    ensure map frame setting is applied to all subplot figures.
    """
    fig_ref, fig_test = Figure(), Figure()
    with fig_ref.subplot(nrows=1, ncols=2, Ff="6c/3c", B="WSne"):
        with fig_ref.set_panel(panel=0):
            fig_ref.basemap(region=[0, 3, 0, 3], frame="+tplot0")
        with fig_ref.set_panel(panel=1):
            fig_ref.basemap(region=[0, 3, 0, 3], frame="+tplot1")
    with fig_test.subplot(nrows=1, ncols=2, figsize=("6c", "3c"), frame="WSne"):
        with fig_test.set_panel(panel="0,0"):
            fig_test.basemap(region=[0, 3, 0, 3], frame="+tplot0")
        with fig_test.set_panel(panel=[0, 1]):
            fig_test.basemap(region=[0, 3, 0, 3], frame="+tplot1")
    return fig_ref, fig_test


@check_figures_equal()
def test_subplot_direct():
    """
    Plot map elements to subplot directly using the panel parameter.
    """
    fig_ref, fig_test = Figure(), Figure()
    with fig_ref.subplot(nrows=2, ncols=1, Fs="3c/3c"):
        fig_ref.basemap(region=[0, 3, 0, 3], frame="af", panel=0)
        fig_ref.basemap(region=[0, 3, 0, 3], frame="af", panel=1)
    with fig_test.subplot(nrows=2, ncols=1, subsize=("3c", "3c")):
        fig_test.basemap(region=[0, 3, 0, 3], frame="af", panel=[0, 0])
        fig_test.basemap(region=[0, 3, 0, 3], frame="af", panel=[1, 0])
    return fig_ref, fig_test


@check_figures_equal()
def test_subplot_autolabel_margins_title():
    """
    Make subplot figure with autolabels, setting some margins and a title.
    """
    fig_ref, fig_test = Figure(), Figure()
    kwargs = dict(nrows=2, ncols=1, figsize=("15c", "6c"))

    with fig_ref.subplot(A="a)", M="0.3c/0.1c", T="Subplot Title", **kwargs):
        fig_ref.basemap(region=[0, 1, 2, 3], frame="WSne", c="0,0")
        fig_ref.basemap(region=[4, 5, 6, 7], frame="WSne", c="1,0")

    with fig_test.subplot(
        autolabel=True, margins=["0.3c", "0.1c"], title="Subplot Title", **kwargs
    ):
        fig_test.basemap(region=[0, 1, 2, 3], frame="WSne", panel=[0, 0])
        fig_test.basemap(region=[4, 5, 6, 7], frame="WSne", panel=[1, 0])

    return fig_ref, fig_test


@check_figures_equal()
def test_subplot_clearance_and_shared_xy_axis_layout():
    """
    Ensure subplot clearance works, and that the layout can be set to use
    shared X and Y axis labels across columns and rows.
    """
    fig_ref, fig_test = Figure(), Figure()
    kwargs = dict(nrows=2, ncols=2, frame="WSrt", figsize=("5c", "5c"))

    with fig_ref.subplot(C="y0.2c", SC="t", SR="", **kwargs):
        fig_ref.basemap(region=[0, 4, 0, 4], projection="X?", panel=True)
        fig_ref.basemap(region=[0, 8, 0, 4], projection="X?", panel=True)
        fig_ref.basemap(region=[0, 4, 0, 8], projection="X?", panel=True)
        fig_ref.basemap(region=[0, 8, 0, 8], projection="X?", panel=True)

    with fig_test.subplot(
        clearance=["s0.2c", "n0.2c"], sharex="t", sharey=True, **kwargs
    ):
        fig_test.basemap(region=[0, 4, 0, 4], projection="X?", panel=True)
        fig_test.basemap(region=[0, 8, 0, 4], projection="X?", panel=True)
        fig_test.basemap(region=[0, 4, 0, 8], projection="X?", panel=True)
        fig_test.basemap(region=[0, 8, 0, 8], projection="X?", panel=True)

    return fig_ref, fig_test


def test_subplot_figsize_and_subsize_error():
    """
    Check that an error is raised when both figsize and subsize parameters are
    passed into subplot.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        with fig.subplot(figsize=("2c", "1c"), subsize=("2c", "1c")):
            pass


def test_subplot_nrows_ncols_less_than_one_error():
    """
    Check that an error is raised when nrows or ncols is less than one.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        with fig.subplot(nrows=0, ncols=-1, figsize=("2c", "1c")):
            pass
