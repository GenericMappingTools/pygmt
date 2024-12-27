"""
Test basic functionality for loading IGPP Earth east-west and south-north deflection
datasets.
"""

import numpy as np
import numpy.testing as npt
from pygmt.datasets import load_earth_deflection


def test_earth_edefl_01d():
    """
    Test some properties of the Earth east-west deflection 01d data.
    """
    data = load_earth_deflection(resolution="01d")
    assert data.name == "z"
    assert data.attrs["long_name"] == "edefl (microradians)"
    assert data.attrs["description"] == "IGPP Earth east-west deflections"
    assert data.attrs["units"] == "micro-radians"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -188.85, atol=0.04)
    npt.assert_allclose(data.max(), 161.25, atol=0.04)


def test_earth_edefl_01d_with_region():
    """
    Test loading low-resolution Earth east-west deflection with "region".
    """
    data = load_earth_deflection(resolution="01d", region=[-10, 10, -5, 5])
    assert data.shape == (11, 21)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -36.125, atol=0.04)
    npt.assert_allclose(data.max(), 45.3, atol=0.04)


def test_earth_edefl_01m_default_registration():
    """
    Test that the grid returned by default for the 1 arc-minute resolution has a "pixel"
    registration.
    """
    data = load_earth_deflection(resolution="01m", region=[-10, -9, 3, 5])
    assert data.shape == (120, 60)
    assert data.gmt.registration == 1
    npt.assert_allclose(data.coords["lat"].data.min(), 3.008333333)
    npt.assert_allclose(data.coords["lat"].data.max(), 4.991666666)
    npt.assert_allclose(data.coords["lon"].data.min(), -9.99166666)
    npt.assert_allclose(data.coords["lon"].data.max(), -9.00833333)
    npt.assert_allclose(data.min(), -49.225, atol=0.04)
    npt.assert_allclose(data.max(), 115.0, atol=0.04)


def test_earth_ndefl_01d():
    """
    Test some properties of the Earth south-north deflection 01d data.
    """
    data = load_earth_deflection(resolution="01d", direction="ndefl")
    assert data.name == "z"
    assert data.attrs["long_name"] == "ndefl (microradians)"
    assert data.attrs["description"] == "IGPP Earth south-north deflections"
    assert data.attrs["units"] == "micro-radians"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -188.85, atol=0.04)
    npt.assert_allclose(data.max(), 161.25, atol=0.04)


def test_earth_ndefl_01d_with_region():
    """
    Test loading low-resolution Earth south-north deflection with "region".
    """
    data = load_earth_deflection(
        resolution="01d", region=[-10, 10, -5, 5], direction="ndefl"
    )
    assert data.shape == (11, 21)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -36.125, atol=0.04)
    npt.assert_allclose(data.max(), 45.3, atol=0.04)


def test_earth_ndefl_01m_default_registration():
    """
    Test that the grid returned by default for the 1 arc-minute resolution has a "pixel"
    registration.
    """
    data = load_earth_deflection(
        resolution="01m", region=[-10, -9, 3, 5], direction="ndefl"
    )
    assert data.shape == (120, 60)
    assert data.gmt.registration == 1
    npt.assert_allclose(data.coords["lat"].data.min(), 3.008333333)
    npt.assert_allclose(data.coords["lat"].data.max(), 4.991666666)
    npt.assert_allclose(data.coords["lon"].data.min(), -9.99166666)
    npt.assert_allclose(data.coords["lon"].data.max(), -9.00833333)
    npt.assert_allclose(data.min(), -49.225, atol=0.04)
    npt.assert_allclose(data.max(), 115.0, atol=0.04)
