"""
Test Figure.subplot.
"""

import pytest
from pygmt import Figure
from pygmt.exceptions import GMTParameterError, GMTValueError
from pygmt.params import Box, Position


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare
def test_subplot_basic_frame():
    """
    Create a subplot figure with 1 vertical row and 2 horizontal columns, and ensure map
    frame setting is applied to all subplot figures.
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
def test_subplot_tag_margins_title():
    """
    Make subplot figure with tags, setting some margins and a title.
    """
    fig = Figure()

    with fig.subplot(
        nrows=2,
        ncols=1,
        figsize=("15c", "6c"),
        tag=True,
        margins=["0.3c", "0.1c"],
        title="Subplot Title",
    ):
        fig.basemap(region=[0, 1, 2, 3], frame="WSne", panel=[0, 0])
        fig.basemap(region=[4, 5, 6, 7], frame="WSne", panel=[1, 0])

    return fig


@pytest.mark.mpl_image_compare
def test_subplot_clearance_and_shared_xy_axis_layout():
    """
    Ensure subplot clearance works, and that the layout can be set to use shared X and Y
    axis labels across columns and rows.
    """
    fig = Figure()
    with fig.subplot(
        nrows=2,
        ncols=2,
        figsize=("5c", "5c"),
        frame="WSrt",
        clearance=["s0.2c", "n0.2c"],
        sharex="top",
        sharey=True,
    ):
        fig.basemap(region=[0, 4, 0, 4], projection="X?", panel=True)
        fig.basemap(region=[0, 8, 0, 4], projection="X?", panel=True)
        fig.basemap(region=[0, 4, 0, 8], projection="X?", panel=True)
        fig.basemap(region=[0, 8, 0, 8], projection="X?", panel=True)
    return fig


def test_subplot_figsize_and_subsize_error():
    """
    Check that an error is raised when both figsize and subsize parameters are passed
    into subplot.
    """
    fig = Figure()
    with pytest.raises(GMTParameterError):
        with fig.subplot(figsize=("2c", "1c"), subsize=("2c", "1c")):
            pass


def test_subplot_nrows_ncols_less_than_one_error():
    """
    Check that an error is raised when nrows or ncols is less than one.
    """
    fig = Figure()
    with pytest.raises(GMTValueError):
        with fig.subplot(nrows=0, ncols=-1, figsize=("2c", "1c")):
            pass


@pytest.mark.mpl_image_compare()
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
    fig.colorbar(
        position=Position("BC", cstype="outside"),
        length=5,
        orientation="horizontal",
        cmap="google/turbo",
        frame=True,
    )
    return fig


def test_subplot_deprecated_autolabel():
    """
    Test that using the deprecated autolabel parameter raises a warning when conflicted
    with tag parameters.
    """
    fig = Figure()
    with pytest.raises(GMTParameterError):
        with fig.subplot(nrows=1, ncols=1, autolabel=True, tag="a)"):
            pass
    with pytest.raises(GMTParameterError):
        with fig.subplot(nrows=1, ncols=1, autolabel=True, tag_box=True):
            pass
    with pytest.raises(GMTParameterError):
        with fig.subplot(nrows=1, ncols=1, autolabel=True, tag_orientation="vertical"):
            pass
    with pytest.raises(GMTParameterError):
        with fig.subplot(nrows=1, ncols=1, autolabel=True, tag_number_style="roman"):
            pass
    with pytest.raises(GMTParameterError):
        with fig.subplot(nrows=1, ncols=1, autolabel=True, tag_position="TL"):
            pass


def test_subplot_invalid_tag_box():
    """
    Test that using an invalid tag_box raises an error.
    """
    fig = Figure()
    # Box properties "inner_pen", "inner_gap", and "radius" are not supported.
    with pytest.raises(GMTValueError):
        with fig.subplot(nrows=1, ncols=1, tag_box=Box(inner_pen="1p")):
            pass
    with pytest.raises(GMTValueError):
        with fig.subplot(nrows=1, ncols=1, tag_box=Box(inner_gap=1, inner_pen="1p")):
            pass
    with pytest.raises(GMTValueError):
        with fig.subplot(nrows=1, ncols=1, tag_box=Box(radius=1)):
            pass
    # Box clearance must be a single value or a tuple of two values.
    with pytest.raises(GMTValueError):
        with fig.subplot(nrows=1, ncols=1, tag_box=Box(clearance=(1, 2, 3, 4))):
            pass


def test_subplot_invalid_tag_position():
    """
    Test that using an invalid tag_position raises an error.
    """
    fig = Figure()
    # Position's cstype must be "inside" or "outside".
    with pytest.raises(GMTValueError):
        with fig.subplot(
            nrows=1, ncols=1, tag_position=Position((1, 1), cstype="mapcoords")
        ):
            pass
    with pytest.raises(GMTValueError):
        with fig.subplot(
            nrows=1, ncols=1, tag_position=Position((1, 1), cstype="boxcoords")
        ):
            pass
    with pytest.raises(GMTValueError):
        with fig.subplot(
            nrows=1, ncols=1, tag_position=Position((1, 1), cstype="plotcoords")
        ):
            pass
