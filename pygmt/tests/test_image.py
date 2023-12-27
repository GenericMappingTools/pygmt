"""
Test Figure.image.
"""
import sys

import pytest
from pygmt import Figure


@pytest.mark.skipif(sys.platform == "win32", reason="crashes on Windows")
@pytest.mark.mpl_image_compare
def test_image():
    """
    Place images on map.
    """
    fig = Figure()
    fig.image(imagefile="@circuit.png", position="x0/0+w2c", box="+pthin,blue")
    return fig
