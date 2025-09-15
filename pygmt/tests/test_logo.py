"""
Test Figure.logo.
"""

import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare
def test_logo():
    """
    Plot the GMT logo as a stand-alone plot.
    """
    fig = Figure()
    fig.logo()
    return fig


@pytest.mark.mpl_image_compare
def test_logo_on_a_map():
    """
    Plot the GMT logo at the upper right corner of a map.
    """
    fig = Figure()
    fig.basemap(region=[-90, -70, 0, 20], projection="M15c", frame=True)
    fig.logo(
        position_type="inside",
        position="TR",
        anchor_offset=(0.25, 0.25),
        width="7.5c",
        box=True,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_logo_position_type():
    """
    Test that the new group of parameters works as expected.
    """
    fig = Figure()
    fig.basemap(region=[-90, -70, 0, 20], projection="M15c", frame=True)
    fig.logo(position_type="inside", position="TL")
    fig.logo(position_type="outside", position="TR")
    fig.logo(position_type="mapcoords", position=(-80, 15))
    fig.logo(position_type="boxcoords", position=(0, 0.5))
    fig.logo(position_type="plotcoords", position=("2c", "0c"), width="5c")
    fig.logo(position=("8c", "0c"))  # Default position_type is "plotcoords".
    return fig


@pytest.mark.mpl_image_compare(filename="test_logo_position_type.png")
def test_logo_position_deprecated_syntax():
    """
    Test that passing the deprecated GMT CLI syntax string to 'position' works.
    """
    fig = Figure()
    fig.basemap(region=[-90, -70, 0, 20], projection="M15c", frame=True)
    fig.logo(position="jTL")
    fig.logo(position="JTR")
    fig.logo(position="g-80/15")
    fig.logo(position="n0/0.5")
    fig.logo(position="x2c/0c+w5c")
    fig.logo(position="8c/0c")
    return fig


def test_logo_width_and_height():
    """
    Test that an error is raised when both width and height are specified.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.logo(width="5c", height="5c")
