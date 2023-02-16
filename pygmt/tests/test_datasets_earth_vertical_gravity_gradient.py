"""
Test basic functionality for loading Earth vertical gravity gradient datasets.
"""
import numpy as np
import numpy.testing as npt
import pytest
from pygmt.datasets import load_earth_vertical_gravity_gradient
from pygmt.exceptions import GMTInvalidInput


def test_earth_vertical_gravity_gradient_fails():
    """
    Make sure load_earth_vertical_gravity_gradient fails for invalid
    resolutions.
    """
    resolutions = "1m 1d bla 60d 001m 03".split()
    resolutions.append(60)
    for resolution in resolutions:
        with pytest.raises(GMTInvalidInput):
            load_earth_vertical_gravity_gradient(resolution=resolution)


def test_earth_vertical_gravity_gradient_incorrect_registration():
    """
    Test loading load_earth_vertical_gravity_gradient with incorrect
    registration type.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_vertical_gravity_gradient(registration="improper_type")


def test_earth_vertical_gravity_gradient_01d():
    """
    Test some properties of the earth vgg 01d data.
    """
    data = load_earth_vertical_gravity_gradient(resolution="01d")
    assert data.name == "earth_vgg"
    assert data.attrs["units"] == "Eotvos"
    assert data.attrs["long_name"] == "IGPP Global Earth Vertical Gravity Gradient"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -136.34375)
    npt.assert_allclose(data.max(), 104.59375)
    assert data[1, 1].isnull()


def test_earth_vertical_gravity_gradient_01d_with_region():
    """
    Test loading low-resolution earth vgg with 'region'.
    """
    data = load_earth_vertical_gravity_gradient(
        resolution="01d", region=[-10, 10, -5, 5]
    )
    assert data.shape == (11, 21)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -16.34375)
    npt.assert_allclose(data.max(), 19.78125)


def test_earth_vertical_gravity_gradient_01m_without_region():
    """
    Test loading high-resolution earth vgg without passing 'region'.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_vertical_gravity_gradient("01m")


def test_earth_vertical_gravity_gradient_incorrect_resolution_registration():
    """
    Test that an error is raised when trying to load a grid registration with
    an unavailable resolution.
    """
    with pytest.raises(GMTInvalidInput):
        load_earth_vertical_gravity_gradient(
            resolution="01m", region=[0, 1, 3, 5], registration="gridline"
        )


def test_earth_vertical_gravity_gradient_01m_default_registration():
    """
    Test that the grid returned by default for the 1 arc-minute resolution has
    a "pixel" registration.
    """
    data = load_earth_vertical_gravity_gradient(
        resolution="01m", region=[-10, -9, 3, 5]
    )
    assert data.shape == (120, 60)
    assert data.gmt.registration == 1
    npt.assert_allclose(data.coords["lat"].data.min(), 3.008333333)
    npt.assert_allclose(data.coords["lat"].data.max(), 4.991666666)
    npt.assert_allclose(data.coords["lon"].data.min(), -9.99166666)
    npt.assert_allclose(data.coords["lon"].data.max(), -9.00833333)
    npt.assert_allclose(data.min(), -40.25)
    npt.assert_allclose(data.max(), 81.75)
