"""
Test basic functionality for loading Earth vertical gravity gradient datasets.
"""

import numpy as np
import numpy.testing as npt
from pygmt.datasets import load_earth_vertical_gravity_gradient


def test_earth_vertical_gravity_gradient_01d():
    """
    Test some properties of the earth vgg 01d data.
    """
    data = load_earth_vertical_gravity_gradient(resolution="01d")
    assert data.name == "z"
    assert data.attrs["long_name"] == "vgg (Eotvos)"
    assert data.attrs["description"] == "IGPP Earth vertical gravity gradient"
    assert data.attrs["units"] == "Eotvos"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -40.1875, atol=1 / 32)
    npt.assert_allclose(data.max(), 45.96875, atol=1 / 32)
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
    npt.assert_allclose(data.min(), -5.34375, atol=1 / 32)
    npt.assert_allclose(data.max(), 5.59375, atol=1 / 32)


def test_earth_vertical_gravity_gradient_01m_default_registration():
    """
    Test that the grid returned by default for the 1 arc-minute resolution has a "pixel"
    registration.
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
    npt.assert_allclose(data.min(), -37.5625, atol=1 / 32)
    npt.assert_allclose(data.max(), 82.59375, atol=1 / 32)
