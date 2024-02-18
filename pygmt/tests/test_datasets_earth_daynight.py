"""
Test basic functionality for loading Blue and Black Marble datasets.
"""
import numpy as np
import numpy.testing as npt
import pytest
from pygmt.datasets import load_blue_marble

rioxarray = pytest.importorskip("rioxarray")


def test_blue_marble_01d():
    """
    Test some properties of the Blue Marble 01d data.
    """
    data = load_blue_marble(resolution="01d")
    assert data.name == "blue_marble"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.attrs["long_name"] == "NASA Day Images"
    assert data.shape == (3, 180, 360)
    assert data.gmt.registration == 1
    assert data.gmt.gtype == 1
    npt.assert_allclose(data.y, np.arange(89.5, -90.5, -1))
    npt.assert_allclose(data.x, np.arange(-179.5, 180.5, 1))
    npt.assert_allclose(data.min(), 10, atol=1)
    npt.assert_allclose(data.max(), 255, atol=1)


def test_blue_marble_01d_with_region():
    """
    Test loading low-resolution Blue Marble with 'region'.
    """
    data = load_blue_marble(resolution="01d", region=[-10, 10, -5, 5])
    assert data.shape == (3, 20, 10)
    assert data.gmt.registration == 1
    assert data.gmt.gtype == 1
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), 0, atol=1)
    npt.assert_allclose(data.max(), 255, atol=1)


def test_blue_marble_01m_default_registration():
    """
    Test that the grid returned by default for the 1 arc-minute resolution has
    a "pixel" registration.
    """
    data = load_blue_marble(resolution="01m", region=[-10, -9, 3, 5])
    assert data.shape == (3, 12, 3)
    assert data.gmt.registration == 1
    assert data.gmt.gtype == 1
    assert data.coords["lat"].data.min() == 3.0
    assert data.coords["lat"].data.max() == 5.0
    assert data.coords["lon"].data.min() == -10.0
    assert data.coords["lon"].data.max() == -9.0
    npt.assert_allclose(data.min(), 0, atol=1)
    npt.assert_allclose(data.max(), 255, atol=1)
