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
    fig.image(imagefile="@circuit.png", position="x0/0+w2c", box=Box(pen="thin,blue"))
    return fig
