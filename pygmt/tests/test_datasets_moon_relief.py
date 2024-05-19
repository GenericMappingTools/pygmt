"""
Test basic functionality for loading Moon relief datasets.
"""

import numpy as np
import numpy.testing as npt
from pygmt.datasets import load_moon_relief


def test_moon_relief_01d():
    """
    Test some properties of the Moon relief 01d data.
    """
    data = load_moon_relief(resolution="01d")
    assert data.name == "z"
    assert data.attrs["long_name"] == "elevation (m)"
    assert data.attrs["description"] == "USGS Moon (LOLA) relief"
    assert data.attrs["units"] == "meters"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -7669.0, atol=0.5)
    npt.assert_allclose(data.max(), 8507.5, atol=0.5)


def test_moon_relief_01d_with_region():
    """
    Test loading low-resolution Moon relief with 'region'.
    """
    data = load_moon_relief(resolution="01d", region=[-10, 10, -5, 5])
    assert data.shape == (11, 21)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -1122.0, atol=0.5)
    npt.assert_allclose(data.max(), 943.0, atol=0.5)


def test_moon_relief_01m_default_registration():
    """
    Test that the grid returned by default for the 1 arc-minute resolution has
    a "gridline" registration.
    """
    data = load_moon_relief(resolution="01m", region=[-10, -9, 3, 5])
    assert data.shape == (121, 61)
    assert data.gmt.registration == 0
    assert data.coords["lat"].data.min() == 3.0
    assert data.coords["lat"].data.max() == 5.0
    assert data.coords["lon"].data.min() == -10.0
    assert data.coords["lon"].data.max() == -9.0
    npt.assert_allclose(data.min(), -1840.5, atol=0.5)
    npt.assert_allclose(data.max(), -235.0, atol=0.5)
