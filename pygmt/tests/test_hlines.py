"""
Tests for Figure.hlines.
"""

import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput


@pytest.mark.mpl_image_compare
def test_hlines_one_line():
    """
    Plot one horizontal line.
    """
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 10], projection="X10c/10c", frame=True)
    fig.hlines(1)
    fig.hlines(2, xmin=1)
    fig.hlines(3, xmax=9)
    fig.hlines(4, xmin=3, xmax=8)
    fig.hlines(5, xmin=4, xmax=8, pen="1p,blue", label="Line at y=5")
    fig.hlines(6, xmin=5, xmax=7, pen="1p,red", label="Line at y=6")
    fig.legend()
    return fig


@pytest.mark.mpl_image_compare
def test_hlines_multiple_lines():
    """
    Plot multiple horizontal lines.
    """
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 16], projection="X10c/10c", frame=True)
    fig.hlines([1, 2])
    fig.hlines([3, 4, 5], xmin=[1, 2, 3])
    fig.hlines([6, 7, 8], xmax=[7, 8, 9])
    fig.hlines([9, 10], xmin=[1, 2], xmax=[9, 10])
    fig.hlines([11, 12], xmin=1, xmax=9, pen="1p,blue", label="Lines at y=11,12")
    fig.hlines(
        [13, 14], xmin=[3, 4], xmax=[8, 9], pen="1p,red", label="Lines at y=13,14"
    )
    fig.legend()
    return fig


@pytest.mark.mpl_image_compare
def test_hlines_clip():
    """
    Plot horizontal lines with clipping or not.
    """
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 4], projection="X10c/4c", frame=True)
    fig.hlines(1, xmin=-2, xmax=12)
    fig.hlines(2, xmin=-2, xmax=12, no_clip=True)
    return fig


@pytest.mark.mpl_image_compare
@pytest.mark.parametrize("region", ["g", "d"])
def test_hlines_geographic_global(region):
    """
    Plot horizontal lines in geographic coordinates.
    """
    fig = Figure()
    fig.basemap(region=region, projection="R15c", frame=True)
    # Plot lines with longitude range of 0 to 360.
    fig.hlines(10, pen="1p")
    fig.hlines(20, xmin=0, xmax=360, pen="1p")
    fig.hlines(30, xmin=0, xmax=180, pen="1p")
    fig.hlines(40, xmin=180, xmax=360, pen="1p")
    fig.hlines(50, xmin=0, xmax=90, pen="1p")
    fig.hlines(60, xmin=90, xmax=180, pen="1p")
    fig.hlines(70, xmin=180, xmax=270, pen="1p")
    fig.hlines(80, xmin=270, xmax=360, pen="1p")

    # Plot lines with longitude range of -180 to 180.
    fig.hlines(-10, pen="1p,red")
    fig.hlines(-20, xmin=-180, xmax=180, pen="1p,red")
    fig.hlines(-30, xmin=-180, xmax=0, pen="1p,red")
    fig.hlines(-40, xmin=0, xmax=180, pen="1p,red")
    fig.hlines(-50, xmin=-180, xmax=-90, pen="1p,red")
    fig.hlines(-60, xmin=-90, xmax=0, pen="1p,red")
    fig.hlines(-70, xmin=0, xmax=90, pen="1p,red")
    fig.hlines(-80, xmin=90, xmax=180, pen="1p,red")
    return fig


@pytest.mark.mpl_image_compare
def test_hlines_polar_projection():
    """
    Plot horizontal lines in polar projection.
    """
    fig = Figure()
    fig.basemap(region=[0, 360, 0, 1], projection="P15c", frame=True)
    fig.hlines(0.1, pen="1p")
    fig.hlines(0.2, xmin=0, xmax=360, pen="1p")
    fig.hlines(0.3, xmin=0, xmax=180, pen="1p")
    fig.hlines(0.4, xmin=180, xmax=360, pen="1p")
    fig.hlines(0.5, xmin=0, xmax=90, pen="1p")
    fig.hlines(0.6, xmin=90, xmax=180, pen="1p")
    fig.hlines(0.7, xmin=180, xmax=270, pen="1p")
    fig.hlines(0.8, xmin=270, xmax=360, pen="1p")
    return fig


def test_hlines_invalid_input():
    """
    Test invalid input for hlines.
    """
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 6], projection="X10c/6c", frame=True)
    with pytest.raises(GMTInvalidInput):
        fig.hlines(1, xmin=2, xmax=[3, 4])
    with pytest.raises(GMTInvalidInput):
        fig.hlines(1, xmin=[2, 3], xmax=4)
    with pytest.raises(GMTInvalidInput):
        fig.hlines(1, xmin=[2, 3], xmax=[4, 5])
    with pytest.raises(GMTInvalidInput):
        fig.hlines([1, 2], xmin=[2, 3, 4], xmax=3)
    with pytest.raises(GMTInvalidInput):
        fig.hlines([1, 2], xmin=[2, 3], xmax=[4, 5, 6])
