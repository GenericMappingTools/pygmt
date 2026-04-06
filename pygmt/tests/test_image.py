"""
Test Figure.image.
"""

import pytest
from pygmt import Figure
from pygmt.exceptions import GMTParameterError
from pygmt.params import Box, Position


@pytest.mark.mpl_image_compare
def test_image():
    """
    Place images on map.
    """
    fig = Figure()
    fig.image(imagefile="@circuit.png")
    return fig


@pytest.mark.mpl_image_compare
def test_image_complete():
    """
    Test all parameters of image.
    """
    fig = Figure()
    fig.image(
        imagefile="@circuit.png",
        position=Position((0, 0)),
        width="4c",
        height=0,
        replicate=(2, 1),
        dpi=300,
        box=Box(pen="thin,blue"),
    )
    return fig


@pytest.mark.mpl_image_compare
def test_image_height_no_width():
    """
    Test all parameters of image.
    """
    fig = Figure()
    fig.image(imagefile="@circuit.png", height=2)
    return fig


@pytest.mark.mpl_image_compare(filename="test_image_complete.png")
def test_image_position_deprecated_syntax():
    """
    Test that passing the deprecated GMT CLI syntax string to 'position' works.
    """
    fig = Figure()
    fig.image(
        imagefile="@circuit.png",
        position="x0/0+w4c/0c+n2/1+r300",
        box=Box(pen="thin,blue"),
    )
    return fig


def test_image_position_mixed_syntax():
    """
    Test that an error is raised when 'position' is given as a raw GMT CLI string
    and conflicts with other parameters.
    """
    fig = Figure()
    with pytest.raises(GMTParameterError):
        fig.image(imagefile="@circuit.png", position="x0/0", width="4c")
    with pytest.raises(GMTParameterError):
        fig.image(imagefile="@circuit.png", position="x0/0", height="3c")
    with pytest.raises(GMTParameterError):
        fig.image(imagefile="@circuit.png", position="x0/0", dpi="300")
    with pytest.raises(GMTParameterError):
        fig.image(imagefile="@circuit.png", position="x0/0", replicate=(2, 1))
