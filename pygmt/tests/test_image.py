"""
Test Figure.image.
"""

import pytest
from pygmt import Figure
from pygmt.params import Box


@pytest.mark.mpl_image_compare
def test_image():
    """
    Place images on map.
    """
    fig = Figure()
    fig.image(
        imagefile="@circuit.png",
        position=(0, 0),
        position_type="x",
        dimension="2c",
        box=Box(pen="thin,blue"),
    )
    return fig
