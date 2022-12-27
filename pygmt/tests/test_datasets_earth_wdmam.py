"""
Test basic functionality for loading the WDMAM magnetic datasets.
"""
import numpy as np
import numpy.testing as npt
import pytest
from pygmt.datasets import load_earth_wdmam
from pygmt.exceptions import GMTInvalidInput


def test_earth_wdmam_fails():
    """
    Make sure earth_magnetic_anomaly fails for invalid resolutions.
    """
    resolutions = "1m 1d bla 60d 001m 03".split()
    resolutions.append(60)
    for resolution in resolutions:
        with pytest.raises(GMTInvalidInput):
            load_earth_wdmam(resolution=resolution)


def test_earth_wdmam_incorrect_registration():
    """
    Test loading earth_magnetic_anomaly with incorrect registration type.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_wdmam(registration="improper_type")


def test_earth_wdmam_01d():
    """
    Test some properties of the WDMAM 01d data.
    """
    data = load_earth_wdmam(resolution="01d", registration="gridline")
    assert data.name == "wdmam"
    assert data.attrs["long_name"] == "World Digital Magnetic Anomaly Map"
    assert data.attrs["units"] == "nT"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -773.5)
    npt.assert_allclose(data.max(), 1751.3)


def test_earth_wdmam_01d_with_region():
    """
    Test loading low-resolution WDMAM grid with 'region'.
    """
    data = load_earth_wdmam(
        resolution="01d", region=[-10, 10, -5, 5], registration="gridline"
    )
    assert data.shape == (11, 21)
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -103.900024)
    npt.assert_allclose(data.max(), 102.19995)


def test_earth_wdmam_03m_with_region():
    """
    Test loading a subregion of high-resolution WDMAM data.
    """
    data = load_earth_wdmam(resolution="03m", region=[10, 13, -60, -58])
    assert data.gmt.registration == 0
    assert data.shape == (41, 61)
    assert data.lat.min() == -60
    assert data.lat.max() == -58
    assert data.lon.min() == 10
    assert data.lon.max() == 13
    npt.assert_allclose(data.min(), -639.7001)
    npt.assert_allclose(data.max(), 629.6)


def test_earth_wdmam_05m_without_region():
    """
    Test loading high-resolution WDMAM without passing 'region'.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_wdmam(resolution="05m", registration="gridline")


def test_earth_wdmam_incorrect_resolution_registration():
    """
    Test that an error is raised when trying to load a grid registration with
    an unavailable resolution.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_wdmam(resolution="03m", region=[0, 1, 3, 5], registration="pixel")
