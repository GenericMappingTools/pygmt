"""
Tests for pygmt.config.
"""
import pytest
from pygmt import Figure, config


@pytest.mark.mpl_image_compare
def test_config():
    """
    Test if config works globally and locally.
    """
    fig = Figure()
    # Change global settings of current figure
    config(FONT_ANNOT_PRIMARY="blue")
    fig.basemap(
        region=[0, 10, 0, 10], projection="X5c/5c", frame=["af", "+tBlue Annotation"]
    )

    with config(FONT_LABEL="red", FONT_ANNOT_PRIMARY="red"):
        fig.shift_origin(xshift="7c")
        fig.basemap(
            region=[0, 10, 0, 10],
            projection="X5c/5c",
            frame=["xaf+lred label", "yaf", "+tred annotation"],
        )

    fig.shift_origin(xshift="7c")
    fig.basemap(
        region=[0, 10, 0, 10],
        projection="X5c/5c",
        frame=["af", "+tBlue Annotation"],
    )
    # Revert to default settings in current figure
    config(FONT_ANNOT_PRIMARY="black")
    return fig


@pytest.mark.mpl_image_compare
def test_config_font_one():
    """
    Test that setting FONT config changes all FONT_* settings except FONT_LOGO.

    Specifically, this test only checks that FONT_ANNOT_PRIMARY,
    FONT_ANNOT_SECONDARY, FONT_LABEL, and FONT_TITLE are modified.
    """
    fig = Figure()
    with config(FONT="8p,red"):
        fig.basemap(region=[0, 9, 0, 9], projection="C3/3/9c", compass="jTL+w3c+d4.5+l")
    fig.basemap(compass="jBR+w3.5c+d-4.5+l")
    return fig


@pytest.mark.mpl_image_compare
def test_config_font_annot():
    """
    Test that setting FONT_ANNOT config changes both FONT_ANNOT_PRIMARY and
    FONT_ANNOT_SECONDARY.
    """
    fig = Figure()
    with config(FONT_ANNOT="6p,red"):
        fig.basemap(region=[0, 9, 0, 9], projection="C3/3/9c", compass="jTL+w3c+d4.5")
    fig.basemap(compass="jBR+w3.5c+d-4.5")
    return fig


@pytest.mark.mpl_image_compare
def test_config_format_date_map():
    """
    Test that setting FORMAT_DATE_MAP config changes how the output date string
    is plotted.

    Note the space in 'o dd', this acts as a regression test for
    https://github.com/GenericMappingTools/pygmt/issues/247.
    """
    fig = Figure()
    with config(FORMAT_DATE_MAP="o dd"):
        fig.basemap(
            region=["1969-7-21T", "1969-7-23T", 0, 1],
            projection="X2.5c/0.1c",
            frame=["sxa1D", "S"],
        )
    return fig


@pytest.mark.mpl_image_compare
def test_config_format_time_map():
    """
    Test that setting FORMAT_TIME_MAP config changes both
    FORMAT_TIME_PRIMARY_MAP and FORMAT_TIME_SECONDARY_MAP.
    """
    fig = Figure()
    with config(FORMAT_TIME_MAP="abbreviation"):
        fig.basemap(
            region=["2020-1-24T", "2020-1-27T", 0, 1],
            projection="X6c/1c",
            frame=["pa1K", "sa1K", "NWse"],
        )
    fig.basemap(frame=["pa1K", "sa1K", "nwSE"])
    return fig


@pytest.mark.mpl_image_compare
def test_config_map_annot_offset():
    """
    Test that setting MAP_ANNOT_OFFSET config changes both
    MAP_ANNOT_OFFSET_PRIMARY and MAP_ANNOT_OFFSET_SECONDARY.
    """
    fig = Figure()
    with config(MAP_ANNOT_OFFSET="15p"):
        fig.basemap(
            region=["2020-1-24T", "2020-1-27T", 0, 1],
            projection="X6c/1c",
            frame=["pa1d", "sa1d", "NWse"],
        )
    fig.basemap(frame=["pa1d", "sa1d", "nwSE"])
    return fig


@pytest.mark.mpl_image_compare
def test_config_map_grid_cross_size():
    """
    Test that setting MAP_GRID_CROSS_SIZE config changes both
    MAP_GRID_CROSS_SIZE_PRIMARY and MAP_GRID_CROSS_SIZE_SECONDARY.
    """
    fig = Figure()
    with config(MAP_GRID_CROSS_SIZE="3p"):
        fig.basemap(
            region=["2020-1-24T21:00", "2020-1-25T00:00", 0, 1],
            projection="X6c/2c",
            frame=["pa1Hg", "sa45mg45m", "NWse"],
            verbose="e",
        )
    fig.shift_origin(yshift=-3)
    fig.basemap(frame=["pa1Hg", "sa45mg45m", "nwSE"], verbose="e")
    return fig


@pytest.mark.mpl_image_compare
def test_config_map_grid_pen():
    """
    Test that setting MAP_GRID_PEN config changes both MAP_GRID_PEN_PRIMARY and
    MAP_GRID_PEN_SECONDARY.
    """
    fig = Figure()
    with config(MAP_GRID_PEN="thick,red"):
        fig.basemap(
            region=["2020-1-24T21:00", "2020-1-25T00:00", 0, 1],
            projection="X6c/2c",
            frame=["pa1Hg", "sa45mg45m", "NWse"],
            verbose="e",
        )
    fig.shift_origin(yshift=-3)
    fig.basemap(frame=["pa1Hg", "sa45mg45m", "nwSE"], verbose="e")
    return fig


@pytest.mark.mpl_image_compare
def test_config_map_tick_length():
    """
    Test that setting MAP_TICK_LENGTH config changes both
    MAP_TICK_LENGTH_PRIMARY and MAP_TICK_LENGTH_SECONDARY.
    """
    fig = Figure()
    with config(MAP_TICK_LENGTH="5p"):
        fig.basemap(
            region=["2020-1-24T21:00", "2020-1-25T00:00", 0, 1],
            projection="X6c/2c",
            frame=["pa1Hg", "sa45mg45m", "NWse"],
            verbose="e",
        )
    fig.shift_origin(yshift=-3)
    fig.basemap(frame=["pa1Hg", "sa45mg45m", "nwSE"], verbose="e")
    return fig


@pytest.mark.mpl_image_compare
def test_config_map_tick_pen():
    """
    Test that setting MAP_TICK_PEN config changes both MAP_TICK_PEN_PRIMARY and
    MAP_TICK_PEN_SECONDARY.
    """
    fig = Figure()
    with config(MAP_TICK_PEN="thick,red"):
        fig.basemap(
            region=["2020-1-24T21:00", "2020-1-25T00:00", 0, 1],
            projection="X6c/2c",
            frame=["pa1Hg", "sa45mg45m", "NWse"],
            verbose="e",
        )
    fig.shift_origin(yshift=-3)
    fig.basemap(frame=["pa1Hg", "sa45mg45m", "nwSE"], verbose="e")
    return fig
