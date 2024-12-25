"""
Test basic functionality for loading Earth mean sea surface datasets.
"""

import numpy as np
import numpy.testing as npt
from pygmt.datasets import load_earth_mean_sea_surface


def test_earth_mss_01d():
    """
    Test some properties of the Earth mean sea surface 01d data.
    """
    data = load_earth_mean_sea_surface(resolution="01d")
    assert data.name == "z"
    assert data.attrs["description"] == "CNES Earth mean sea surface"
    assert data.attrs["units"] == "m"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -2655.7, atol=0.01)
    npt.assert_allclose(data.max(), 2463.42, atol=0.01)


def test_earth_mss_01d_with_region():
    """
    Test loading low-resolution Earth mean sea surface with "region".
    """
    data = load_earth_mean_sea_surface(resolution="01d", region=[-10, 10, -5, 5])
    assert data.shape == (11, 21)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -1081.94, atol=0.01)
    npt.assert_allclose(data.max(), 105.18, atol=0.01)


def test_earth_mss_01m_default_registration():
    """
    Test that the grid returned by default for the 1 arc-minute resolution has a
    "gridline" registration.
    """
    data = load_earth_mean_sea_surface(resolution="01m", region=[-10, -9, 3, 5])
    assert data.shape == (121, 61)
    assert data.gmt.registration == 0
    assert data.coords["lat"].data.min() == 3.0
    assert data.coords["lat"].data.max() == 5.0
    assert data.coords["lon"].data.min() == -10.0
    assert data.coords["lon"].data.max() == -9.0
    npt.assert_allclose(data.min(), -243.62, atol=0.01)
    npt.assert_allclose(data.max(), 2.94, atol=0.01)
