"""
Test basic functionality for loading Earth free air anomaly datasets.
"""
import numpy as np
import numpy.testing as npt
import pytest
from pygmt.datasets import load_earth_free_air_anomaly
from pygmt.exceptions import GMTInvalidInput


def test_earth_faa_fails():
    """
    Make sure earth_free_air_anomaly fails for invalid resolutions.
    """
    resolutions = "1m 1d bla 60d 001m 03".split()
    resolutions.append(60)
    for resolution in resolutions:
        with pytest.raises(GMTInvalidInput):
            load_earth_free_air_anomaly(resolution=resolution)


def test_earth_faa_incorrect_registration():
    """
    Test loading earth_free_air_anomaly with incorrect registration type.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_free_air_anomaly(registration="improper_type")


def test_earth_faa_01d():
    """
    Test some properties of the free air anomaly 01d data.
    """
    data = load_earth_free_air_anomaly(resolution="01d")
    assert data.name == "free_air_anomaly"
    assert data.attrs["long_name"] == "IGPP Global Earth Free-Air Anomaly"
    assert data.attrs["units"] == "mGal"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -275.75)
    npt.assert_allclose(data.max(), 308.375)


def test_earth_faa_01d_with_region():
    """
    Test loading low-resolution earth free air anomaly with 'region'.
    """
    data = load_earth_free_air_anomaly(resolution="01d", region=[-10, 10, -5, 5])
    assert data.shape == (11, 21)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -58.75)
    npt.assert_allclose(data.max(), 69.524994)


def test_earth_faa_01m_without_region():
    """
    Test loading high-resolution earth free air anomaly without passing
    'region'.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_free_air_anomaly("01m")


def test_earth_faa_01m_default_registration():
    """
    Test that the grid returned by default for the 1 arc-minute resolution has
    a "pixel" registration.
    """
    data = load_earth_free_air_anomaly(resolution="01m", region=[-10, -9, 3, 5])
    assert data.shape == (120, 60)
    assert data.gmt.registration == 1
    npt.assert_allclose(data.coords["lat"].data.min(), 3.008333333)
    npt.assert_allclose(data.coords["lat"].data.max(), 4.991666666)
    npt.assert_allclose(data.coords["lon"].data.min(), -9.99166666)
    npt.assert_allclose(data.coords["lon"].data.max(), -9.00833333)
    npt.assert_allclose(data.min(), -51)
    npt.assert_allclose(data.max(), 113.675)
