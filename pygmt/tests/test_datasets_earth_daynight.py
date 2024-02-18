"""
Test basic functionality for loading Blue and Black Marble datasets.
"""
import numpy as np
import numpy.testing as npt
from pygmt.datasets import load_blue_marble


def test_blue_marble_01d():
    """
    Test some properties of the Blue Marble 01d data.
    """
    data = load_blue_marble(resolution="01d")
    assert data.name == "blue_marble"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.attrs["long_name"] == "NASA Day Images"
    assert data.shape == (3, 180, 360)
    assert data.gmt.registration == 1
    assert data.gmt.gtype == 1
    npt.assert_allclose(data.y, np.arange(89.5, -90.5, -1))
    npt.assert_allclose(data.x, np.arange(-179.5, 180.5, 1))
    npt.assert_allclose(data.min(), 10, atol=1)
    npt.assert_allclose(data.max(), 255, atol=1)
