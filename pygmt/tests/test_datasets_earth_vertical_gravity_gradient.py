"""
Test basic functionality for loading Earth vertical gravity gradient datasets.
"""
import numpy as np
import numpy.testing as npt
import pytest
from pygmt.datasets import load_earth_vgg
from pygmt.exceptions import GMTInvalidInput


def test_earth_vgg_fails():
    """
    Make sure load_earth_vgg fails for invalid resolutions.
    """
    resolutions = "1m 1d bla 60d 001m 03".split()
    resolutions.append(60)
    for resolution in resolutions:
        with pytest.raises(GMTInvalidInput):
            load_earth_vgg(resolution=resolution)


def test_earth_vgg_incorrect_registration():
    """
    Test loading load_earth_vgg with incorrect registration type.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_vgg(registration="improper_type")


def test_earth_vgg_01d():
    """
    Test some properties of the earth vgg 01d data.
    """
    data = load_earth_vgg(resolution="01d", registration="gridline")
    assert data.name == "earth_vgg"
    assert data.attrs["units"] == "Eotvos"
    assert data.attrs["long_name"] == "IGPP Global Earth Vertical Gravity Gradient"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -136.34375)
    npt.assert_allclose(data.max(), 104.59375)
    assert data[1, 1].isnull()


def test_earth_vgg_01d_with_region():
    """
    Test loading low-resolution earth vgg with 'region'.
    """
    data = load_earth_vgg(
        resolution="01d", region=[-10, 10, -5, 5], registration="gridline"
    )
    assert data.shape == (11, 21)
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -16.34375)
    npt.assert_allclose(data.max(), 19.78125)


def test_earth_vgg_05m_with_region():
    """
    Test loading a subregion of high-resolution earth vgg.
    """
    data = load_earth_vgg(
        resolution="05m", region=[-50, -40, 20, 26], registration="gridline"
    )
    assert data.coords["lat"].data.min() == 20.0
    assert data.coords["lat"].data.max() == 26.0
    assert data.coords["lon"].data.min() == -50.0
    assert data.coords["lon"].data.max() == -40.0
    npt.assert_allclose(data.min(), -107.625)
    npt.assert_allclose(data.max(), 159.75)
    assert data.sizes["lat"] == 73
    assert data.sizes["lon"] == 121


def test_earth_vgg_05m_without_region():
    """
    Test loading high-resolution earth vgg without passing 'region'.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_vgg("05m")


def test_earth_vgg_incorrect_resolution_registration():
    """
    Test that an error is raised when trying to load a grid registration with
    an unavailable resolution.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_vgg(resolution="01m", region=[0, 1, 3, 5], registration="pixel")
