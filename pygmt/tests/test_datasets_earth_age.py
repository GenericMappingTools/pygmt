"""
Test basic functionality for loading Earth seafloor crust age datasets.
"""
import numpy as np
import numpy.testing as npt
import pytest
from pygmt.datasets import load_earth_age
from pygmt.exceptions import GMTInvalidInput


def test_earth_age_fails():
    """
    Make sure earth_age fails for invalid resolutions.
    """
    resolutions = "1m 1d bla 60d 001m 03".split()
    resolutions.append(60)
    for resolution in resolutions:
        with pytest.raises(GMTInvalidInput):
            load_earth_age(resolution=resolution)


def test_earth_age_incorrect_registration():
    """
    Test loading earth_age with incorrect registration type.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_age(registration="improper_type")


def test_earth_age_01d():
    """
    Test some properties of the earth age 01d data.
    """
    data = load_earth_age(resolution="01d")
    assert data.name == "seafloor_age"
    assert data.attrs["units"] == "Myr"
    assert data.attrs["long_name"] == "age of seafloor crust"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), 0.167381, rtol=1e-5)
    npt.assert_allclose(data.max(), 338.0274, rtol=1e-5)


def test_earth_age_01d_with_region():
    """
    Test loading low-resolution earth age with 'region'.
    """
    data = load_earth_age(resolution="01d", region=[-10, 10, -5, 5])
    assert data.shape == (11, 21)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), 11.293945)
    npt.assert_allclose(data.max(), 125.1189)


def test_earth_age_01m_without_region():
    """
    Test loading high-resolution earth age without passing 'region'.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_age("01m")


def test_earth_age_incorrect_resolution_registration():
    """
    Test that an error is raised when trying to load a grid registration with
    an unavailable resolution.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_age(resolution="01m", region=[0, 1, 3, 5], registration="pixel")


def test_earth_age_01m_default_registration():
    """
    Test that the grid returned by default for the 1 arc-minute resolution has
    a "gridline" registration.
    """
    data = load_earth_age(resolution="01m", region=[-10, -9, 3, 5])
    assert data.shape == (121, 61)
    assert data.gmt.registration == 0
    assert data.coords["lat"].data.min() == 3.0
    assert data.coords["lat"].data.max() == 5.0
    assert data.coords["lon"].data.min() == -10.0
    assert data.coords["lon"].data.max() == -9.0
    npt.assert_allclose(data.min(), 88.63)
    npt.assert_allclose(data.max(), 125.25)
