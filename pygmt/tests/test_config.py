"""
Tests for gmt config
"""
import pytest

from .. import Figure, config


@pytest.mark.mpl_image_compare
def test_config():
    """
    Test if config works globally and locally.
    """
    # Change global settings
    config(FONT_ANNOT_PRIMARY="blue")
    fig = Figure()
    fig.basemap(
        region="0/10/0/10", projection="X10c/10c", frame=["af", '+t"Blue Annotation"']
    )

    with config(FONT_LABEL="red", FONT_ANNOT_PRIMARY="red"):
        fig.basemap(
            region="0/10/0/10",
            projection="X10c/10c",
            frame=['xaf+l"red label"', "yaf", '+t"red annotation"'],
            X="15c",
        )

    fig.basemap(
        region="0/10/0/10",
        projection="X10c/10c",
        frame=["af", '+t"Blue Annotation"'],
        X="15c",
    )
    # Revert to default settings
    config(FONT_ANNOT_PRIMARY="black")
    return fig


@pytest.mark.mpl_image_compare
def test_config_font_one():
    """
    Test that setting `FONT` config changes all `FONT_*` settings except
    `FONT_LOGO`. Specifically, this test only checks that `FONT_ANNOT_PRIMARY`,
    `FONT_ANNOT_SECONDARY`, `FONT_LABEL`, and `FONT_TITLE` are modified.
    """
    fig = Figure()
    with config(FONT="8p,red"):
        fig.basemap(region=[0, 9, 0, 9], projection="C3/3/9c", T="mjTL+w4c+d4.5+l")
    fig.basemap(T="mjBR+w5c+d-4.5+l")
    return fig


@pytest.mark.mpl_image_compare
def test_config_font_annot():
    """
    Test that setting `FONT_ANNOT` config changes both `FONT_ANNOT_PRIMARY` and
    `FONT_ANNOT_SECONDARY`.
    """
    fig = Figure()
    with config(FONT_ANNOT="6p,red"):
        fig.basemap(region=[0, 9, 0, 9], projection="C3/3/9c", T="mjTL+w4c+d4.5")
    fig.basemap(T="mjBR+w5c+d-4.5")
    return fig


@pytest.mark.mpl_image_compare
def test_config_format_time_map():
    """
    Test that setting `FORMAT_TIME_MAP` config changes both
    `FORMAT_TIME_PRIMARY_MAP` and `FORMAT_TIME_SECONDARY_MAP`.
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
    Test that setting `MAP_ANNOT_OFFSET` config changes both
    `MAP_ANNOT_OFFSET_PRIMARY` and `MAP_ANNOT_OFFSET_SECONDARY`.
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
    Test that setting `MAP_GRID_CROSS_SIZE` config changes both
    `MAP_GRID_CROSS_SIZE_PRIMARY` and `MAP_GRID_CROSS_SIZE_SECONDARY`.
    """
    fig = Figure()
    config(
        MAP_GRID_CROSS_SIZE_PRIMARY="0p", MAP_GRID_CROSS_SIZE_SECONDARY="0p"
    )  # Remove after https://github.com/GenericMappingTools/gmt/issues/3062 is fixed
    with config(MAP_GRID_CROSS_SIZE="3p"):
        fig.basemap(
            region=["2020-1-24T21:00", "2020-1-25T00:00", 0, 1],
            projection="X6c/2c",
            frame=["pa1Hg", "sa45mg45m", "NWse"],
        )
    fig.basemap(frame=["pa1Hg", "sa45mg45m", "nwSE"], Y=-3)
    return fig


@pytest.mark.mpl_image_compare
def test_config_map_grid_pen():
    """
    Test that setting `MAP_GRID_PEN` config changes both
    `MAP_GRID_PEN_PRIMARY` and `MAP_GRID_PEN_SECONDARY`.
    """
    fig = Figure()
    with config(MAP_GRID_PEN="thick,red"):
        fig.basemap(
            region=["2020-1-24T21:00", "2020-1-25T00:00", 0, 1],
            projection="X6c/2c",
            frame=["pa1Hg", "sa45mg45m", "NWse"],
        )
    fig.basemap(frame=["pa1Hg", "sa45mg45m", "nwSE"], Y=-3)
    return fig


@pytest.mark.mpl_image_compare
def test_config_map_tick_length():
    """
    Test that setting `MAP_TICK_LENGTH` config changes both
    `MAP_TICK_LENGTH_PRIMARY` and `MAP_TICK_LENGTH_SECONDARY`.
    """
    fig = Figure()
    with config(MAP_TICK_LENGTH="5p"):
        fig.basemap(
            region=["2020-1-24T21:00", "2020-1-25T00:00", 0, 1],
            projection="X6c/2c",
            frame=["pa1Hg", "sa45mg45m", "NWse"],
        )
    fig.basemap(frame=["pa1Hg", "sa45mg45m", "nwSE"], Y=-3)
    return fig


@pytest.mark.mpl_image_compare
def test_config_map_tick_pen():
    """
    Test that setting `MAP_TICK_PEN` config changes both
    `MAP_TICK_PEN_PRIMARY` and `MAP_TICK_PEN_SECONDARY`.
    """
    fig = Figure()
    with config(MAP_TICK_PEN="thick,red"):
        fig.basemap(
            region=["2020-1-24T21:00", "2020-1-25T00:00", 0, 1],
            projection="X6c/2c",
            frame=["pa1Hg", "sa45mg45m", "NWse"],
        )
    fig.basemap(frame=["pa1Hg", "sa45mg45m", "nwSE"], Y=-3)
    return fig
