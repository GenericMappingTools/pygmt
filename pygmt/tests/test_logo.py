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


def test_logo_width_and_height():
    """
    Test that an error is raised when both width and height are specified.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.logo(width="5c", height="5c")
