"""
Tests for Figure.vlines.
"""

import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput


@pytest.mark.mpl_image_compare
def test_vlines_one_line():
    """
    Plot one vertical line.
    """
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 10], projection="X10c/10c", frame=True)
    fig.vlines(1)
    fig.vlines(2, ymin=1)
    fig.vlines(3, ymax=9)
    fig.vlines(4, ymin=3, ymax=8)
    fig.vlines(5, ymin=4, ymax=8, pen="1p,blue", label="Line at x=5")
    fig.vlines(6, ymin=5, ymax=7, pen="1p,red", label="Line at x=6")
    fig.legend()
    return fig


@pytest.mark.mpl_image_compare
def test_vlines_multiple_lines():
    """
    Plot multiple vertical lines.
    """
    fig = Figure()
    fig.basemap(region=[0, 16, 0, 10], projection="X10c/10c", frame=True)
    fig.vlines([1, 2])
    fig.vlines([3, 4, 5], ymin=[1, 2, 3])
    fig.vlines([6, 7, 8], ymax=[7, 8, 9])
    fig.vlines([9, 10], ymin=[1, 2], ymax=[9, 10])
    fig.vlines([11, 12], ymin=1, ymax=8, pen="1p,blue", label="Lines at x=11,12")
    fig.vlines(
        [13, 14], ymin=[3, 4], ymax=[7, 8], pen="1p,red", label="Lines at x=13,14"
    )
    fig.legend()
    return fig


@pytest.mark.mpl_image_compare
def test_vlines_clip():
    """
    Plot vertical lines with clipping or not.
    """
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 4], projection="X10c/4c", frame=True)
    fig.vlines(1, ymin=-1, ymax=5)
    fig.vlines(2, ymin=-1, ymax=5, no_clip=True)
    return fig


@pytest.mark.mpl_image_compare
def test_vlines_geographic_global():
    """
    Plot vertical lines in geographic coordinates.
    """
    fig = Figure()
    fig.basemap(region=[-180, 180, -90, 90], projection="R15c", frame="a30g30")
    fig.vlines(30, pen="1p")
    fig.vlines(90, ymin=-60, pen="1p,blue")
    fig.vlines(-90, ymax=60, pen="1p,blue")
    fig.vlines(120, ymin=-60, ymax=60, pen="1p,blue")
    return fig


@pytest.mark.mpl_image_compare
def test_vlines_polar_projection():
    """
    Plot vertical lines in polar projection.
    """
    fig = Figure()
    fig.basemap(region=[0, 360, 0, 1], projection="P15c", frame=True)
    fig.vlines(0, pen="1p")
    fig.vlines(30, ymin=0, ymax=1, pen="1p")
    fig.vlines(60, ymin=0.5, pen="1p")
    fig.vlines(90, ymax=0.5, pen="1p")
    fig.vlines(120, ymin=0.25, ymax=0.75, pen="1p")
    return fig


def test_vlines_invalid_input():
    """
    Test invalid input for vlines.
    """
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 6], projection="X10c/6c", frame=True)
    with pytest.raises(GMTInvalidInput):
        fig.vlines(1, ymin=2, ymax=[3, 4])
    with pytest.raises(GMTInvalidInput):
        fig.vlines(1, ymin=[2, 3], ymax=4)
    with pytest.raises(GMTInvalidInput):
        fig.vlines(1, ymin=[2, 3], ymax=[4, 5])
    with pytest.raises(GMTInvalidInput):
        fig.vlines([1, 2], ymin=[2, 3, 4], ymax=3)
    with pytest.raises(GMTInvalidInput):
        fig.vlines([1, 2], ymin=[2, 3], ymax=[4, 5, 6])
