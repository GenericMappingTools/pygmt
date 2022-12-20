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
    data = load_earth_free_air_anomaly(resolution="01d", registration="gridline")
    assert data.name == "free_air_anomaly"
    assert data.attrs["long_name"] == "IGPP Global Earth Free-Air Anomaly"
    assert data.attrs["units"] == "mGal"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -275.75)
    npt.assert_allclose(data.max(), 308.375)


def test_earth_faa_01d_with_region():
    """
    Test loading low-resolution earth free air anomaly with 'region'.
    """
    data = load_earth_free_air_anomaly(
        resolution="01d", region=[-10, 10, -5, 5], registration="gridline"
    )
    assert data.shape == (11, 21)
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -58.75)
    npt.assert_allclose(data.max(), 69.524994)


def test_earth_faa_05m_with_region():
    """
    Test loading a subregion of high-resolution earth free air anomaly data.
    """
    data = load_earth_free_air_anomaly(
        resolution="05m", region=[-115, -112, 4, 6], registration="gridline"
    )
    assert data.shape == (25, 37)
    assert data.lat.min() == 4
    assert data.lat.max() == 6
    assert data.lon.min() == -115
    assert data.lon.max() == -112
    npt.assert_allclose(data.min(), -20.5)
    npt.assert_allclose(data.max(), -3.9500122)


def test_earth_faa_05m_without_region():
    """
    Test loading high-resolution earth free air anomaly without passing
    'region'.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_free_air_anomaly("05m")
