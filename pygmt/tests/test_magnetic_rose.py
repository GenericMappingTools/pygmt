"""
Test Figure.magnetic_rose.
"""

import pytest
from pygmt import Figure
from pygmt.exceptions import GMTParameterError
from pygmt.params import Position


@pytest.mark.mpl_image_compare
def test_magnetic_rose():
    """
    Create a map with a compass. Modified from the test_basemap_compass test.
    """
    fig = Figure()
    fig.basemap(region=[127.5, 128.5, 26, 27], projection="M10c", frame=True)
    fig.magnetic_rose()
    return fig


@pytest.mark.mpl_image_compare
def test_magnetic_rose_complete():
    """
    Test all parameters of Figure.magnetic_rose.
    """
    fig = Figure()
    fig.basemap(region=[-10, 10, -10, 10], projection="M10c", frame=True)
    fig.magnetic_rose(
        position=Position("BL"),
        width="2c",
        labels=["W", "E", "S", "*"],
        intervals=(45, 15, 3, 60, 20, 4),
        outer_pen="1p,red",
        inner_pen="1p,blue",
        declination=11.5,
        declination_label="11.5 °E",
    )
    return fig


def test_magnetic_rose_invalid_declination_label():
    """
    Test that an exception is raised when declination_label is set but declination is
    not set.
    """
    fig = Figure()
    fig.basemap(region=[-10, 10, -10, 10], projection="M10c", frame=True)
    with pytest.raises(GMTParameterError):
        fig.magnetic_rose(declination_label="11.5°E")
