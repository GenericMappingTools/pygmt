"""
Test basic functionality for loading Earth mean dynamic topography datasets.
"""

import numpy as np
import numpy.testing as npt
from pygmt.datasets import load_earth_mean_dynamic_topography


def test_earth_mdt_01d():
    """
    Test some properties of the Earth mean dynamic topography 01d data.
    """
    data = load_earth_mean_dynamic_topography(resolution="01d")
    assert data.name == "z"
    assert data.attrs["description"] == "CNES Earth mean dynamic topography"
    assert data.attrs["units"] == "meters"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -1.4668, atol=0.0001)
    npt.assert_allclose(data.max(), 1.7151, atol=0.0001)


def test_earth_mdt_01d_with_region():
    """
    Test loading low-resolution Earth mean dynamic topography with "region".
    """
    data = load_earth_mean_dynamic_topography(resolution="01d", region=[-10, 10, -5, 5])
    assert data.shape == (11, 21)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), 0.346, atol=0.0001)
    npt.assert_allclose(data.max(), 0.4839, atol=0.0001)


def test_earth_mdt_07m_default_registration():
    """
    Test that the grid returned by default for the 7 arc-minutes resolution has a
    "gridline" registration.
    """
    data = load_earth_mean_dynamic_topography(resolution="07m", region=[-10, -9, 3, 5])
    assert data.shape == (17, 9)
    assert data.gmt.registration == 0
    assert data.coords["lat"].data.min() == 3.0
    assert data.coords["lat"].data.max() == 5.0
    assert data.coords["lon"].data.min() == -10.0
    assert data.coords["lon"].data.max() == -9.0
    npt.assert_allclose(data.min(), 0.4138, atol=0.0001)
    npt.assert_allclose(data.max(), 0.4302, atol=0.0001)
