"""
Test Figure.scalebar.
"""

import pytest
from pygmt import Figure
from pygmt.params import Position


@pytest.mark.mpl_image_compare
def test_scalebar():
    """
    Create a map with a scale bar.
    """
    fig = Figure()
    fig.basemap(region=[100, 120, 20, 30], projection="M10c", frame=True)
    fig.scalebar(length=500)
    return fig


@pytest.mark.mpl_image_compare
def test_scalebar_complete():
    """
    Test all parameters of scalebar.
    """
    fig = Figure()
    fig.basemap(region=[100, 120, 20, 30], projection="M10c", frame=True)
    fig.scalebar(
        length=1000,
        height="10p",
        position=Position((110, 22), cstype="mapcoords"),
        fancy=True,
        label="Scale",
        label_alignment="left",
        scale_at=(110, 25),
        unit=True,
        box=True,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_scalebar_cartesian():
    """
    Test scale bar in Cartesian coordinates.
    """
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 5], projection="X10c/5c", frame=True)
    fig.scalebar(length=1, position=Position((2, 1), cstype="mapcoords"))
    fig.scalebar(length=1, position=Position((4, 1), cstype="mapcoords"), vertical=True)
    return fig
