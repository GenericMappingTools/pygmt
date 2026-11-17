"""
Test Figure.directional_rose.
"""

import pytest
from pygmt import Figure
from pygmt.exceptions import GMTParameterError
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


@pytest.mark.mpl_image_compare
def test_directional_rose_upright_labels():
    """
    Test the Figure.directional_rose method with upright labels.

    The rose is placed where the map is rotated by more than 90 degrees, so that the
    labels would otherwise be upside down.
    """
    fig = Figure()
    fig.basemap(region=[-180, 180, 60, 90], projection="S0/90/6c", frame=True)
    fig.directional_rose(position="TC", width=2, fancy=1, labels=True)
    fig.shift_origin(xshift="w+1")
    fig.basemap(region=[-180, 180, 60, 90], projection="S0/90/6c", frame=True)
    fig.directional_rose(
        position="TC", width=2, fancy=1, labels=True, upright_labels=True
    )
    return fig


def test_directional_rose_upright_labels_fails():
    """
    Test that upright_labels requires both fancy and labels to be set.
    """
    fig = Figure()
    fig.basemap(region=[0, 80, 0, 30], projection="M10c", frame=True)
    with pytest.raises(GMTParameterError):
        fig.directional_rose(upright_labels=True)
    with pytest.raises(GMTParameterError):
        fig.directional_rose(upright_labels=True, fancy=1)
    with pytest.raises(GMTParameterError):
        fig.directional_rose(upright_labels=True, labels=["W", "E", "S", "N"])
