"""
Test basic functionality for loading Black Marble datasets.
"""

import numpy as np
import numpy.testing as npt
from pygmt.datasets import load_black_marble


def test_black_marble_01d():
    """
    Test some properties of the Black Marble 01d data.
    """
    data = load_black_marble(resolution="01d")
    assert data.name == "z"
    assert data.long_name == "black_marble"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.attrs["description"] == "NASA Night Images"
    assert data.shape == (3, 180, 360)
    assert data.dtype == "uint8"
    assert data.gmt.registration == 1
    assert data.gmt.gtype == 1
    npt.assert_allclose(data.y, np.arange(89.5, -90.5, -1))
    npt.assert_allclose(data.x, np.arange(-179.5, 180.5, 1))
    npt.assert_allclose(data.min(), 3, atol=1)
    npt.assert_allclose(data.max(), 174, atol=1)


def test_black_marble_01d_with_region():
    """
    Test loading low-resolution Black Marble with 'region'.
    """
    data = load_black_marble(resolution="01d", region=[-10, 10, -5, 5])
    assert data.shape == (3, 10, 20)
    assert data.dtype == "uint8"
    assert data.gmt.registration == 1
    assert data.gmt.gtype == 1
    npt.assert_allclose(data.y, np.arange(4.5, -5.5, -1))
    npt.assert_allclose(data.x, np.arange(-9.5, 10.5, 1))
    npt.assert_allclose(data.min(), 3, atol=1)
    npt.assert_allclose(data.max(), 40, atol=1)
