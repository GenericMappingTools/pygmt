"""
Test Figure.directional_rose.
"""

import pytest
from pygmt import Figure


@pytest.mark.mpl_image_compare(filename="test_basemap_rose.png")
def test_directional_rose():
    """
    Test the Figure.directional_rose method.
    """
    fig = Figure()
    fig.basemap(region=[127.5, 128.5, 26, 27], projection="H15c", frame=True)
    fig.directional_rose(position="MC", position_type="inside", width="5c")
    return fig


@pytest.mark.mpl_image_compare
def test_directional_rose_complex():
    """
    Test the Figure.directional_rose method with more parameters.
    """
    fig = Figure()
    fig.basemap(region=[0, 80, -30, 30], projection="M10c", frame=True)
    fig.directional_rose(
        position=(50, 0),
        position_type="mapcoords",
        width="1c",
        label=["", "", "", "N"],
        fancy=2,
        anchor_offset=(1, 1),
        justify="MC",
    )
    return fig
