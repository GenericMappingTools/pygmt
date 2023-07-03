"""
Test Figure.subplot.
"""
import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput


@pytest.mark.mpl_image_compare
def test_subplot_basic_frame():
    """
    Create a subplot figure with 1 vertical row and 2 horizontal columns, and
    ensure map frame setting is applied to all subplot figures.
    """
    fig = Figure()

    with fig.subplot(nrows=1, ncols=2, figsize=("6c", "3c"), frame="WSne"):
        with fig.set_panel(panel="0,0"):
            fig.basemap(region=[0, 3, 0, 3], frame="+tplot0")
        with fig.set_panel(panel=[0, 1]):
            fig.basemap(region=[0, 3, 0, 3], frame="+tplot1")
    return fig


@pytest.mark.mpl_image_compare
def test_subplot_direct():
    """
    Plot map elements to subplot directly using the panel parameter.
    """
    fig = Figure()

    with fig.subplot(nrows=2, ncols=1, subsize=("3c", "3c")):
        fig.basemap(region=[0, 3, 0, 3], frame="af", panel=[0, 0])
        fig.basemap(region=[0, 3, 0, 3], frame="af", panel=[1, 0])
    return fig


@pytest.mark.mpl_image_compare
def test_subplot_autolabel_margins_title():
    """
    Make subplot figure with autolabels, setting some margins and a title.
    """
    fig = Figure()

    with fig.subplot(
        nrows=2,
        ncols=1,
        figsize=("15c", "6c"),
        autolabel=True,
        margins=["0.3c", "0.1c"],
        title="Subplot Title",
    ):
        fig.basemap(region=[0, 1, 2, 3], frame="WSne", panel=[0, 0])
        fig.basemap(region=[4, 5, 6, 7], frame="WSne", panel=[1, 0])

    return fig


@pytest.mark.mpl_image_compare
def test_subplot_clearance_and_shared_xy_axis_layout():
    """
    Ensure subplot clearance works, and that the layout can be set to use
    shared X and Y axis labels across columns and rows.
    """
    fig = Figure()

    with fig.subplot(
        nrows=2,
        ncols=2,
        figsize=("5c", "5c"),
        frame="WSrt",
        clearance=["s0.2c", "n0.2c"],
        sharex="t",
        sharey=True,
    ):
        fig.basemap(region=[0, 4, 0, 4], projection="X?", panel=True)
        fig.basemap(region=[0, 8, 0, 4], projection="X?", panel=True)
        fig.basemap(region=[0, 4, 0, 8], projection="X?", panel=True)
        fig.basemap(region=[0, 8, 0, 8], projection="X?", panel=True)

    return fig


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


# Increase tolerance for compatibility with GMT 6.3 and 6.4, see
# https://github.com/GenericMappingTools/pygmt/pull/2454
@pytest.mark.mpl_image_compare(tolerance=4.0)
def test_subplot_outside_plotting_positioning():
    """
    Plotting calls are correctly positioned after exiting subplot.

    This is a regression test for
    https://github.com/GenericMappingTools/pygmt/issues/2426.
    """
    fig = Figure()
    with fig.subplot(nrows=1, ncols=2, figsize=(10, 5)):
        fig.basemap(region=[0, 10, 0, 10], projection="X?", panel=True)
        fig.basemap(region=[0, 10, 0, 10], projection="X?", panel=True)
    fig.colorbar(position="JBC+w5c+h", cmap="turbo", frame=True)
    return fig
