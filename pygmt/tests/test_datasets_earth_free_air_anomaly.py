"""
Test basic functionality for loading Earth free air anomaly datasets.
"""
import numpy as np
import numpy.testing as npt
from pygmt.datasets import load_earth_free_air_anomaly


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
    npt.assert_allclose(data.min(), -275.85, atol=0.025)
    npt.assert_allclose(data.max(), 308.35, atol=0.025)


def test_earth_faa_01d_with_region():
    """
    Test loading low-resolution earth free air anomaly with 'region'.
    """
    data = load_earth_free_air_anomaly(resolution="01d", region=[-10, 10, -5, 5])
    assert data.shape == (11, 21)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -58.475, atol=0.025)
    npt.assert_allclose(data.max(), 69.975, atol=0.025)


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
    npt.assert_allclose(data.min(), -49.225, atol=0.025)
    npt.assert_allclose(data.max(), 115.0, atol=0.025)
