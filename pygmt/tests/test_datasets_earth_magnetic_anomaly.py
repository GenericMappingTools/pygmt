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


def test_earth_mag_05m_with_region():
    """
    Test loading a subregion of high-resolution earth magnetic anomaly data.
    """
    data = load_earth_magnetic_anomaly(
        resolution="05m", region=[-115, -112, 4, 6], registration="gridline"
    )
    assert data.shape == (25, 37)
    assert data.lat.min() == 4
    assert data.lat.max() == 6
    assert data.lon.min() == -115
    assert data.lon.max() == -112
    npt.assert_allclose(data.min(), -189.20001)
    npt.assert_allclose(data.max(), 107)


def test_earth_mag_05m_without_region():
    """
    Test loading high-resolution earth magnetic anomaly without passing
    'region'.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_magnetic_anomaly("05m")


def test_earth_mag_incorrect_resolution_registration():
    """
    Test that an error is raised when trying to load a grid registration with
    an unavailable resolution.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_magnetic_anomaly(
            resolution="02m", region=[0, 1, 3, 5], registration="gridline", mag4km=False
        )


def test_earth_mag4km_01d():
    """
    Test some properties of the magnetic anomaly 4km 01d data.
    """
    data = load_earth_magnetic_anomaly(
        resolution="01d", registration="gridline", mag4km=True
    )
    assert data.name == "magnetic_anomaly"
    assert data.attrs["long_name"] == "Earth magnetic anomaly"
    assert data.attrs["units"] == "nT"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -799.19995)
    npt.assert_allclose(data.max(), 3226.4)


def test_earth_mag4km_01d_with_region():
    """
    Test loading low-resolution earth magnetic anomaly 4km 01d with 'region'.
    """
    data = load_earth_magnetic_anomaly(
        resolution="01d",
        region=[-10, 10, -5, 5],
        registration="gridline",
        mag4km=True,
    )
    assert data.shape == (11, 21)
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -153.19995)
    npt.assert_allclose(data.max(), 113.59985)


def test_earth_mag4km_05m_with_region():
    """
    Test loading a subregion of high-resolution earth magnetic anomaly 4km
    data.
    """
    data = load_earth_magnetic_anomaly(
        resolution="05m",
        region=[-115, -112, 4, 6],
        registration="gridline",
        mag4km=True,
    )
    assert data.shape == (25, 37)
    assert data.lat.min() == 4
    assert data.lat.max() == 6
    assert data.lon.min() == -115
    assert data.lon.max() == -112
    npt.assert_allclose(data.min(), -128.40015)
    npt.assert_allclose(data.max(), 76.80005)
