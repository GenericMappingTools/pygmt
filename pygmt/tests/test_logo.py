"""
Test Figure.logo.
"""

import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput
from pygmt.params import Position


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
def test_logo_default_position():
    """
    Test that the default position is at the plot origin when no position is specified.
    """
    fig = Figure()
    fig.basemap(region=[-90, -70, 0, 20], projection="M15c", frame=True)
    fig.logo()
    return fig


@pytest.mark.mpl_image_compare
def test_logo_on_a_map():
    """
    Plot the GMT logo at the upper right corner of a map.
    """
    fig = Figure()
    fig.basemap(region=[-90, -70, 0, 20], projection="M15c", frame=True)
    fig.logo(position=Position("TR", offset=(0.25, 0.25)), width="7.5c", box=True)
    return fig


@pytest.mark.mpl_image_compare(filename="test_logo_on_a_map.png")
def test_logo_position_deprecated_syntax():
    """
    Test that passing the deprecated GMT CLI syntax string to 'position' works.
    """
    fig = Figure()
    fig.basemap(region=[-90, -70, 0, 20], projection="M15c", frame=True)
    fig.logo(position="jTR+o0.25/0.25+w7.5c", box=True)
    return fig


def test_logo_width_and_height():
    """
    Test that an error is raised when both width and height are specified.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.logo(width="5c", height="5c")


def test_logo_position_mixed_syntax():
    """
    Test that an error is raised when mixing new and deprecated syntax in 'position'.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.logo(position="jTL", width="5c")
    with pytest.raises(GMTInvalidInput):
        fig.logo(position="jTL", height="6c")
