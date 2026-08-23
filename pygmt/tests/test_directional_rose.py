"""
Test Figure.directional_rose.
"""

import pytest
from pygmt import Figure
from pygmt.params import Position


@pytest.mark.mpl_image_compare
def test_directional_rose():
    """
    Test the Figure.directional_rose method with default position and width.
    """
    fig = Figure()
    fig.basemap(region=[0, 80, 0, 30], projection="M10c", frame=True)
    fig.directional_rose()
    return fig


@pytest.mark.mpl_image_compare
def test_directional_rose_fancy():
    """
    Test the Figure.directional_rose method with the fancy style enabled.
    """
    fig = Figure()
    fig.basemap(region=[0, 80, 0, 30], projection="M10c", frame=True)
    fig.directional_rose(fancy=True)
    return fig


@pytest.mark.mpl_image_compare
def test_directional_rose_complex():
    """
    Test the Figure.directional_rose method with more parameters.
    """
    fig = Figure()
    fig.basemap(region=[0, 80, 0, 30], projection="M10c", frame=True)
    fig.directional_rose(
        position=Position((50, 0), cstype="mapcoords", anchor="MC", offset=(1, 1)),
        width="1c",
        labels=["", "", "", "N"],
        fancy=2,
    )
    return fig
