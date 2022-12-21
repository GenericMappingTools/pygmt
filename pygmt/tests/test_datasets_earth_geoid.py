"""
Test basic functionality for loading Earth geoid datasets.
"""
import numpy as np
import numpy.testing as npt
import pytest
from pygmt.datasets import load_earth_geoid
from pygmt.exceptions import GMTInvalidInput


def test_earth_geoid_fails():
    """
    Make sure load_earth_geoid fails for invalid resolutions.
    """
    resolutions = "1m 1d bla 60d 001m 03".split()
    resolutions.append(60)
    for resolution in resolutions:
        with pytest.raises(GMTInvalidInput):
            load_earth_geoid(resolution=resolution)


def test_earth_geoid_incorrect_registration():
    """
    Test loading load_earth_geoid with incorrect registration type.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_geoid(registration="improper_type")


def test_earth_geoid_01d():
    """
    Test some properties of the earth geoid 01d data.
    """
    data = load_earth_geoid(resolution="01d", registration="gridline")
    assert data.name == "earth_geoid"
    assert data.attrs["units"] == "m"
    assert data.attrs["long_name"] == "EGM2008 Global Earth Geoid"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -106.45)
    npt.assert_allclose(data.max(), 83.619995)


def test_earth_geoid_01d_with_region():
    """
    Test loading low-resolution earth geoid with 'region'.
    """
    data = load_earth_geoid(
        resolution="01d", region=[-10, 10, -5, 5], registration="gridline"
    )
    assert data.shape == (11, 21)
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), 4.87)
    npt.assert_allclose(data.max(), 29.89)


def test_earth_geoid_05m_with_region():
    """
    Test loading a subregion of high-resolution earth geoid.
    """
    data = load_earth_geoid(
        resolution="05m", region=[-50, -40, 20, 30], registration="gridline"
    )
    assert data.coords["lat"].data.min() == 20.0
    assert data.coords["lat"].data.max() == 30.0
    assert data.coords["lon"].data.min() == -50.0
    assert data.coords["lon"].data.max() == -40.0
    npt.assert_allclose(data.min(), -32.79)
    npt.assert_allclose(data.max(), 16.57)
    assert data.sizes["lat"] == 121
    assert data.sizes["lon"] == 121


def test_earth_geoid_05m_without_region():
    """
    Test loading high-resolution earth geoid without passing 'region'.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_geoid("05m")


def test_earth_geoid_incorrect_resolution_registration():
    """
    Test that an error is raised when trying to load a grid registration with
    an unavailable resolution.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_geoid(resolution="01m", region=[0, 1, 3, 5], registration="pixel")
