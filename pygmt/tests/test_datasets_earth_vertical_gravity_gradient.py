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
    assert data.name == "earth_vgg"
    assert data.attrs["units"] == "Eotvos"
    assert data.attrs["long_name"] == "IGPP Earth Vertical Gravity Gradient"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    assert data[1, 1].isnull()  # noqa: PD003  # ruff's bug


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
