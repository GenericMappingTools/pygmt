"""
Tests subplot.
"""
from pygmt import Figure
from pygmt.helpers.testing import check_figures_equal


@check_figures_equal()
def test_subplot_basic_frame():
    """
    Create a subplot figure with 1 vertical row and 2 horizontal columns, and
    ensure map frame setting is applied to all subplot figures.
    """
    fig_ref, fig_test = Figure(), Figure()
    with fig_ref.subplot(nrows=1, ncols=2, Ff="6c/3c", B="WSne"):
        with fig_ref.sca(ax=0):
            fig_ref.basemap(region=[0, 3, 0, 3], frame="+tplot0")
        with fig_ref.sca(ax=1):
            fig_ref.basemap(region=[0, 3, 0, 3], frame="+tplot1")
    with fig_test.subplot(nrows=1, ncols=2, figsize=("6c", "3c"), frame="WSne"):
        with fig_test.sca(ax=[0, 0]):
            fig_test.basemap(region=[0, 3, 0, 3], frame="+tplot0")
        with fig_test.sca(ax=[0, 1]):
            fig_test.basemap(region=[0, 3, 0, 3], frame="+tplot1")
    return fig_ref, fig_test


@check_figures_equal()
def test_subplot_direct():
    """
    Plot map elements to subplot directly using ax argument.
    """
    fig_ref, fig_test = Figure(), Figure()
    with fig_ref.subplot(nrows=2, ncols=1, Fs="3c/3c"):
        fig_ref.basemap(region=[0, 3, 0, 3], frame="af", ax=0)
        fig_ref.basemap(region=[0, 3, 0, 3], frame="af", ax=1)
    with fig_test.subplot(nrows=2, ncols=1, subsize=("3c", "3c")):
        fig_test.basemap(region=[0, 3, 0, 3], frame="af", ax=[0, 0])
        fig_test.basemap(region=[0, 3, 0, 3], frame="af", ax=[1, 0])
    return fig_ref, fig_test


@check_figures_equal()
def test_subplot_autolabel_margins_title():
    """
    Make subplot figure with autolabels, setting some margins and a title.
    """
    fig_ref, fig_test = Figure(), Figure()
    kwargs = dict(nrows=2, ncols=1, figsize=("15c", "6c"))

    with fig_ref.subplot(A="(1)", M="0.3c/0.1c", T='"Subplot Title"', **kwargs):
        fig_ref.basemap(region=[0, 1, 2, 3], frame="WSne", c="0,0")
        fig_ref.basemap(region=[4, 5, 6, 7], frame="WSne", c="1,0")

    with fig_test.subplot(
        autolabel="(1)", margins=["0.3c", "0.1c"], title='"Subplot Title"', **kwargs
    ):
        fig_test.basemap(region=[0, 1, 2, 3], frame="WSne", ax=[0, 0])
        fig_test.basemap(region=[4, 5, 6, 7], frame="WSne", ax=[1, 0])

    return fig_ref, fig_test


@check_figures_equal()
def test_subplot_clearance_and_shared_xy_axis_layout():
    """
    Ensure subplot clearance works, and that the layout can be set to use
    shared X and Y axis labels across columns and rows.
    """
    fig_ref, fig_test = Figure(), Figure()
    kwargs = dict(nrows=2, ncols=2, frame="WSrt", figsize=("5c", "5c"))

    with fig_ref.subplot(C="y0.2", SR="l", SC="t", **kwargs):
        fig_ref.basemap(region=[0, 4, 0, 4], projection="X?", ax=True)
        fig_ref.basemap(region=[0, 8, 0, 4], projection="X?", ax=True)
        fig_ref.basemap(region=[0, 4, 0, 8], projection="X?", ax=True)
        fig_ref.basemap(region=[0, 8, 0, 8], projection="X?", ax=True)

    with fig_test.subplot(clearance="y0.2", layout=["Rl", "Ct"], **kwargs):
        fig_test.basemap(region=[0, 4, 0, 4], projection="X?", ax=True)
        fig_test.basemap(region=[0, 8, 0, 4], projection="X?", ax=True)
        fig_test.basemap(region=[0, 4, 0, 8], projection="X?", ax=True)
        fig_test.basemap(region=[0, 8, 0, 8], projection="X?", ax=True)

    return fig_ref, fig_test
