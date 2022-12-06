"""
Test basic functionality for loading Earth magnetic anomaly datasets.
"""
import numpy as np
import numpy.testing as npt
import pytest
from pygmt.datasets import load_earth_magnetic_anomaly
from pygmt.exceptions import GMTInvalidInput


def test_earth_mag_fails():
    """
    Make sure earth_magnetic_anomaly fails for invalid resolutions.
    """
    resolutions = "1m 1d bla 60d 001m 03".split()
    resolutions.append(60)
    for resolution in resolutions:
        with pytest.raises(GMTInvalidInput):
            load_earth_magnetic_anomaly(resolution=resolution)


def test_earth_mag_incorrect_registration():
    """
    Test loading earth_magnetic_anomaly with incorrect registration type.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_magnetic_anomaly(registration="improper_type")


def test_earth_mag_01d():
    """
    Test some properties of the magnetic anomaly 01d data.
    """
    data = load_earth_magnetic_anomaly(resolution="01d", registration="gridline")
    assert data.name == "magnetic_anomaly"
    assert data.attrs["long_name"] == "Earth magnetic anomaly"
    assert data.attrs["units"] == "nT"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -384)
    npt.assert_allclose(data.max(), 1057.2)


def test_earth_mag_01d_with_region():
    """
    Test loading low-resolution earth magnetic anomaly with 'region'.
    """
    data = load_earth_magnetic_anomaly(
        resolution="01d", region=[-10, 10, -5, 5], registration="gridline"
    )
    assert data.shape == (11, 21)
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -180.40002)
    npt.assert_allclose(data.max(), 127.39996)


def test_earth_mag_04m_with_region():
    """
    Test loading a subregion of high-resolution earth magnetic anomaly data.
    """
    data = load_earth_magnetic_anomaly(
        resolution="03m", region=[-115, -112, 4, 6], registration="gridline"
    )
    assert data.shape == (41, 61)
    npt.assert_allclose(data.lat, np.arange(4, 6.01, 0.05))
    npt.assert_allclose(data.lon, np.arange(-115, -111.99, 0.05))
    npt.assert_allclose(data.data.min(), -193)
    npt.assert_allclose(data.data.max(), 110)


def test_earth_mag_05m_without_region():
    """
    Test loading high-resolution earth magnetic anomaly without passing
    'region'.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_magnetic_anomaly("05m")
