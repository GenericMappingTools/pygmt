"""
Test Figure.image.
"""

import pytest
from pygmt import Figure
from pygmt.exceptions import GMTParameterError, GMTValueError
from pygmt.params import Box, Frame, Position


@pytest.mark.mpl_image_compare
def test_image():
    """
    Place images on the figure.
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


@pytest.mark.mpl_image_compare
def test_image_bgcolor_fgcolor():
    """
    Test setting the background and foreground colors of a 1-bit image.
    """
    fig = Figure()
    fig.basemap(region=[-1, 8, 0, 5], projection="X10c/5c", frame=Frame(fill="gray"))
    fig.image(imagefile="@vader1.png", position=(0, 0), width="2c")
    fig.image(imagefile="@vader1.png", position=(2, 0), width="2c", bgcolor="")
    fig.image(imagefile="@vader1.png", position=(4, 0), width="2c", fgcolor="")
    fig.image(imagefile="@vader1.png", position=(6, 0), width="2c", bgcolor="red")
    fig.image(imagefile="@vader1.png", position=(0, 2), width="2c", fgcolor="blue")
    fig.image(
        imagefile="@vader1.png",
        position=(2, 2),
        width="2c",
        bgcolor="red",
        fgcolor="blue",
    )
    fig.image(
        imagefile="@vader1.png",
        position=(4, 2),
        width="2c",
        bgcolor="red",
        fgcolor="",
    )
    fig.image(
        imagefile="@vader1.png",
        position=(6, 2),
        width="2c",
        bgcolor="",
        fgcolor="blue",
    )
    return fig


def test_image_bitcolor_invalid():
    """
    Test that invalid 'bgcolor'/'fgcolor'/'transparent_color' values raise an error.
    """
    fig = Figure()
    # Making both the background and the foreground transparent leaves nothing to paint.
    with pytest.raises(GMTValueError):
        fig.image(imagefile="@circuit.png", bgcolor="", fgcolor="")
    # GMT requires a color for the "+t" modifier.
    with pytest.raises(GMTValueError):
        fig.image(imagefile="@circuit.png", transparent_color="")


# TODO(PyGMT>=0.24.0): Remove the test for the deprecated "bitcolor" parameter.
def test_image_bitcolor_deprecated():
    """
    Test that the deprecated 'bitcolor' parameter still works but warns.
    """
    fig = Figure()
    with pytest.warns(FutureWarning):
        fig.image(imagefile="@circuit.png", bitcolor="red+b")
    with pytest.warns(FutureWarning):
        fig.image(imagefile="@circuit.png", bitcolor=["red+b", "blue+f"])


# TODO(PyGMT>=0.24.0): Remove the test for the deprecated "bitcolor" parameter.
def test_image_bitcolor_conflict():
    """
    Test that the deprecated 'bitcolor' parameter raises an error when used with
    'bgcolor', 'fgcolor', or 'transparent_color'.
    """
    fig = Figure()
    with pytest.raises(GMTParameterError):
        with pytest.warns(FutureWarning):
            fig.image(imagefile="@circuit.png", bitcolor="red+b", bgcolor="blue")
    with pytest.raises(GMTParameterError):
        with pytest.warns(FutureWarning):
            fig.image(imagefile="@circuit.png", bitcolor="red+b", fgcolor="blue")
    with pytest.raises(GMTParameterError):
        with pytest.warns(FutureWarning):
            fig.image(
                imagefile="@circuit.png", bitcolor="red+b", transparent_color="blue"
            )
