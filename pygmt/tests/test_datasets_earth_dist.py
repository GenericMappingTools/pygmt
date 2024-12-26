"""
Test basic functionality for loading Earth distance to shoreline datasets.
"""

import numpy as np
import numpy.testing as npt
from pygmt.datasets import load_earth_dist


def test_earth_dist_01d():
    """
    Test some properties of the Earth distance to shoreline 01d data.
    """
    data = load_earth_dist(resolution="01d")
    assert data.name == "z"
    assert data.attrs["description"] == "GSHHG Earth distance to shoreline"
    assert data.attrs["units"] == "kilometers"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -2655.7, atol=0.01)
    npt.assert_allclose(data.max(), 2463.42, atol=0.01)


def test_earth_dist_01d_with_region():
    """
    Test loading low-resolution Earth distance to shoreline with "region".
    """
    data = load_earth_dist(resolution="01d", region=[-10, 10, -5, 5])
    assert data.shape == (11, 21)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -1081.94, atol=0.01)
    npt.assert_allclose(data.max(), 105.18, atol=0.01)


def test_earth_dist_01m_default_registration():
    """
    Test that the grid returned by default for the 1 arc-minute resolution has a
    "gridline" registration.
    """
    data = load_earth_dist(resolution="01m", region=[-10, -9, 3, 5])
    assert data.shape == (121, 61)
    assert data.gmt.registration == 0
    assert data.coords["lat"].data.min() == 3.0
    assert data.coords["lat"].data.max() == 5.0
    assert data.coords["lon"].data.min() == -10.0
    assert data.coords["lon"].data.max() == -9.0
    npt.assert_allclose(data.min(), -243.62, atol=0.01)
    npt.assert_allclose(data.max(), 2.94, atol=0.01)
