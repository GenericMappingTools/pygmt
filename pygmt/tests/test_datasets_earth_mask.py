"""
Test basic functionality for loading Earth mask datasets.
"""

import numpy as np
import numpy.testing as npt
from pygmt.datasets import load_earth_mask


def test_earth_mask_01d():
    """
    Test some properties of the Earth mask 01d data.
    """
    data = load_earth_mask(resolution="01d")
    assert data.name == "z"
    assert data.attrs["description"] == "GSHHG Earth mask"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    assert data.gmt.gtype == 1
    assert data.dtype == "int8"
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), 0)
    npt.assert_allclose(data.max(), 2)
    npt.assert_allclose(data[36, 45], 0)


def test_earth_mask_01d_with_region():
    """
    Test loading low-resolution Earth mask with 'region'.
    """
    data = load_earth_mask(resolution="01d", region=[-7, 4, 13, 19])
    assert data.shape == (7, 12)
    assert data.gmt.registration == 0
    assert data.gmt.gtype == 1
    assert data.dtype == "int8"
    npt.assert_allclose(data.lat, np.arange(13, 20, 1))
    npt.assert_allclose(data.lon, np.arange(-7, 5, 1))
    npt.assert_allclose(data[1, 5], 1)
