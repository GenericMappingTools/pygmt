"""
Test Figure.scalebar.
"""

import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput
from pygmt.params import Position


@pytest.mark.mpl_image_compare
def test_scalebar():
    """
    Create a map with a scale bar.
    """
    fig = Figure()
    fig.basemap(region=[100, 120, 20, 30], projection="M10c", frame=True)
    fig.scalebar(position=Position((118, 22), cstype="mapcoords"), length=200)
    return fig


@pytest.mark.mpl_image_compare
def test_scalebar_complete():
    """
    Test all parameters of scalebar.
    """
    fig = Figure()
    fig.basemap(region=[100, 120, 20, 30], projection="M10c", frame=True)
    fig.scalebar(
        position=Position((110, 22), cstype="mapcoords"),
        length=1000,
        fancy=True,
        label="Scale",
        label_alignment="left",
        scale_position=(110, 25),
        unit=True,
        box=True,
    )
    return fig


def test_scalebar_no_position():
    """
    Test that an error is raised when position is not provided.
    """
    fig = Figure()
    fig.basemap(region=[100, 120, 20, 30], projection="M10c", frame=True)
    with pytest.raises(GMTInvalidInput):
        fig.scalebar(length=200)


def test_scalebar_no_length():
    """
    Test that an error is raised when length is not provided.
    """
    fig = Figure()
    fig.basemap(region=[100, 120, 20, 30], projection="M10c", frame=True)
    with pytest.raises(GMTInvalidInput):
        fig.scalebar(position=Position((118, 22), cstype="mapcoords"))
