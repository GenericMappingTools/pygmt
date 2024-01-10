"""
Test basic functionality for loading Earth geoid datasets.
"""
import numpy as np
import numpy.testing as npt
from pygmt.datasets import load_earth_geoid


def test_earth_geoid_01d():
    """
    Test some properties of the earth geoid 01d data.
    """
    data = load_earth_geoid(resolution="01d")
    assert data.name == "earth_geoid"
    assert data.attrs["units"] == "m"
    assert data.attrs["long_name"] == "EGM2008 Earth Geoid"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))


def test_earth_geoid_01d_with_region():
    """
    Test loading low-resolution earth geoid with 'region'.
    """
    data = load_earth_geoid(resolution="01d", region=[-10, 10, -5, 5])
    assert data.shape == (11, 21)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))


def test_earth_geoid_01m_default_registration():
    """
    Test that the grid returned by default for the 1 arc-minute resolution has a
    "gridline" registration.
    """
    data = load_earth_geoid(resolution="01m", region=[-10, -9, 3, 5])
    assert data.shape == (121, 61)
    assert data.gmt.registration == 0
    assert data.coords["lat"].data.min() == 3.0
    assert data.coords["lat"].data.max() == 5.0
    assert data.coords["lon"].data.min() == -10.0
    assert data.coords["lon"].data.max() == -9.0
