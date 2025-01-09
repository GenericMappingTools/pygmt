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
    assert data.attrs["description"] == "IGPP Earth east-west deflection"
    assert data.attrs["units"] == "micro-radians"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -142.64, atol=0.04)
    npt.assert_allclose(data.max(), 178.32, atol=0.04)


def test_earth_edefl_01d_with_region():
    """
    Test loading low-resolution Earth east-west deflection with "region".
    """
    data = load_earth_deflection(resolution="01d", region=[-10, 10, -5, 5])
    assert data.shape == (11, 21)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -28.92, atol=0.04)
    npt.assert_allclose(data.max(), 24.72, atol=0.04)


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
    npt.assert_allclose(data.min(), -62.24, atol=0.04)
    npt.assert_allclose(data.max(), 15.52, atol=0.04)


def test_earth_ndefl_01d():
    """
    Test some properties of the Earth north-south deflection 01d data.
    """
    data = load_earth_deflection(resolution="01d", component="north")
    assert data.name == "z"
    assert data.attrs["long_name"] == "ndefl (microradians)"
    assert data.attrs["description"] == "IGPP Earth north-south deflection"
    assert data.attrs["units"] == "micro-radians"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.shape == (181, 361)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -214.8, atol=0.04)
    npt.assert_allclose(data.max(), 163.04, atol=0.04)


def test_earth_ndefl_01d_with_region():
    """
    Test loading low-resolution Earth north-south deflection with "region".
    """
    data = load_earth_deflection(
        resolution="01d", region=[-10, 10, -5, 5], component="north"
    )
    assert data.shape == (11, 21)
    assert data.gmt.registration == 0
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), -48.08, atol=0.04)
    npt.assert_allclose(data.max(), 18.92, atol=0.04)


def test_earth_ndefl_01m_default_registration():
    """
    Test that the grid returned by default for the 1 arc-minute resolution has a "pixel"
    registration.
    """
    data = load_earth_deflection(
        resolution="01m", region=[-10, -9, 3, 5], component="north"
    )
    assert data.shape == (120, 60)
    assert data.gmt.registration == 1
    npt.assert_allclose(data.coords["lat"].data.min(), 3.008333333)
    npt.assert_allclose(data.coords["lat"].data.max(), 4.991666666)
    npt.assert_allclose(data.coords["lon"].data.min(), -9.99166666)
    npt.assert_allclose(data.coords["lon"].data.max(), -9.00833333)
    npt.assert_allclose(data.min(), -107.04, atol=0.04)
    npt.assert_allclose(data.max(), 20.28, atol=0.04)
