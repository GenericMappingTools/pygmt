"""
Tests subplot
"""
import pytest

from ..helpers.testing import check_figures_equal
from ..subplot import SubPlot, subplots


@pytest.mark.mpl_image_compare
def test_subplot_basic():
    """
    Create a subplot figure with 1 row and 2 columns.
    """
    fig, axs = subplots(nrows=1, ncols=2, figsize=("6c", "3c"))
    fig.sca(ax=axs[0, 0])
    fig.basemap(region=[0, 3, 0, 3], frame=True)
    fig.sca(ax=axs[0, 1])
    fig.basemap(region=[0, 3, 0, 3], frame=True)
    fig.end_subplot()
    return fig


@pytest.mark.mpl_image_compare
def test_subplot_frame():
    """
    Check that map frame setting is applied to all subplot figures
    """
    fig, axs = subplots(nrows=1, ncols=2, figsize=("6c", "3c"), frame="WSne")
    fig.sca(ax=axs[0, 0])
    fig.basemap(region=[0, 3, 0, 3], frame="+tplot0")
    fig.sca(ax=axs[0, 1])
    fig.basemap(region=[0, 3, 0, 3], frame="+tplot1")
    fig.end_subplot()
    return fig


@pytest.mark.mpl_image_compare
def test_subplot_direct():
    """
    Plot map elements to subplots directly using ax argument
    """
    fig, axs = subplots(nrows=2, ncols=1, figsize=("3c", "6c"))
    fig.basemap(region=[0, 3, 0, 3], frame=True, ax=axs[0, 0])
    fig.basemap(region=[0, 3, 0, 3], frame=True, ax=axs[1, 0])
    fig.end_subplot()
    return fig


@check_figures_equal()
def test_subplot_autolabel_margins_title():
    """
    Make subplot figure with autolabels, setting some margins and a title.
    """
    kwargs = dict(nrows=2, ncols=1, figsize=("15c", "6c"))

    fig_ref = SubPlot(A="(1)", M="0.3c/0.1c", T='"Subplot Title"', **kwargs)
    fig_ref.basemap(region=[0, 1, 2, 3], frame="WSne", c="0,0")
    fig_ref.basemap(region=[4, 5, 6, 7], frame="WSne", c="1,0")
    fig_ref.end_subplot()

    fig_test, axs_test = subplots(
        autolabel="(1)", margins=["0.3c", "0.1c"], title="Subplot Title", **kwargs
    )
    fig_test.basemap(region=[0, 1, 2, 3], frame="WSne", ax=axs_test[0, 0])
    fig_test.basemap(region=[4, 5, 6, 7], frame="WSne", ax=axs_test[1, 0])
    fig_test.end_subplot()

    return fig_ref, fig_test


@check_figures_equal()
def test_subplot_clearance_and_shared_xy_axis_layout():
    """
    Ensure subplot clearance works, and that the layout can be set to use
    shared X and Y axis labels across columns and rows.
    """
    kwargs = dict(nrows=2, ncols=2, frame="WSrt", figsize=("5c", "5c"))

    fig_ref = SubPlot(C="y0.2", SR="l", SC="t", **kwargs)
    fig_test, _ = subplots(clearance="y0.2", layout=["Rl", "Ct"], **kwargs)

    for fig in (fig_ref, fig_test):
        fig.basemap(region=[0, 4, 0, 4], projection="X?", ax=True)
        fig.basemap(region=[0, 8, 0, 4], projection="X?", ax=True)
        fig.basemap(region=[0, 4, 0, 8], projection="X?", ax=True)
        fig.basemap(region=[0, 8, 0, 8], projection="X?", ax=True)
        fig.end_subplot()

    return fig_ref, fig_test
