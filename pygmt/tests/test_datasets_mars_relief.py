"""
Test basic functionality for loading Mars relief datasets.
"""

import numpy as np
import numpy.testing as npt
from pygmt.datasets import load_mars_relief


def test_mars_relief_01d():
    """
    Test some properties of the Mars relief 01d data.
    """
    data = load_mars_relief(resolution="01d")
    assert data.name == "z"
    assert data.attrs["long_name"] == "elevation (m)"
    assert data.attrs["description"] == "NASA Mars (MOLA) relief"
    assert data.attrs["units"] == "meters"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -7421.0, atol=0.5)
    npt.assert_allclose(data.max(), 19587.5, atol=0.5)


def test_mars_relief_01d_with_region():
    """
    Test loading low-resolution Mars relief with 'region'.
    """
    data = load_mars_relief(resolution="01d", region=[-10, 10, -5, 5])
    assert data.shape == (11, 21)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -2502.0, atol=0.5)
    npt.assert_allclose(data.max(), -135.5, atol=0.5)


def test_mars_relief_01m_default_registration():
    """
    Test that the grid returned by default for the 1 arc-minute resolution has
    a "gridline" registration.
    """
    data = load_mars_relief(resolution="01m", region=[-10, -9, 3, 5])
    assert data.shape == (121, 61)
    assert data.gmt.registration == 0
    assert data.coords["lat"].data.min() == 3.0
    assert data.coords["lat"].data.max() == 5.0
    assert data.coords["lon"].data.min() == -10.0
    assert data.coords["lon"].data.max() == -9.0
    npt.assert_allclose(data.min(), -3374.0, atol=0.5)
    npt.assert_allclose(data.max(), -1181.0, atol=0.5)
