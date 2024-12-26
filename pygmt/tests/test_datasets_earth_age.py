"""
Test basic functionality for loading Earth seafloor crust age datasets.
"""

import numpy as np
import numpy.testing as npt
from pygmt.datasets import load_earth_age


def test_earth_age_01d():
    """
    Test some properties of the earth age 01d data.
    """
    data = load_earth_age(resolution="01d")
    assert data.name == "z"
    assert data.attrs["long_name"] == "ages (Myr)"
    assert data.attrs["description"] == "EarthByte Earth seafloor crustal age"
    assert data.attrs["units"] == "Myr"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), 0.37, atol=0.01)
    npt.assert_allclose(data.max(), 336.52, atol=0.01)


def test_earth_age_01d_with_region():
    """
    Test loading low-resolution earth age with 'region'.
    """
    data = load_earth_age(resolution="01d", region=[-10, 10, -5, 5])
    assert data.shape == (11, 21)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), 11.13, atol=0.01)
    npt.assert_allclose(data.max(), 124.64, atol=0.01)


def test_earth_age_01m_default_registration():
    """
    Test that the grid returned by default for the 1 arc-minute resolution has a
    "gridline" registration.
    """
    data = load_earth_age(resolution="01m", region=[-10, -9, 3, 5])
    assert data.shape == (121, 61)
    assert data.gmt.registration == 0
    assert data.coords["lat"].data.min() == 3.0
    assert data.coords["lat"].data.max() == 5.0
    assert data.coords["lon"].data.min() == -10.0
    assert data.coords["lon"].data.max() == -9.0
    npt.assert_allclose(data.min(), 88.63, atol=0.01)
    npt.assert_allclose(data.max(), 125.25, atol=0.01)
