"""
Test basic functionality for loading Earth seafloor crust age datasets.
"""
import numpy as np
import numpy.testing as npt
import pytest
from pygmt.datasets import load_seafloor_crust_age
from pygmt.exceptions import GMTInvalidInput


def test_seafloor_crust_age_fails():
    """
    Make sure seafloor_crust_age fails for invalid resolutions.
    """
    resolutions = "1m 1d bla 60d 001m 03".split()
    resolutions.append(60)
    for resolution in resolutions:
        with pytest.raises(GMTInvalidInput):
            load_seafloor_crust_age(resolution=resolution)


def test_seafloor_crust_age_incorrect_registration():
    """
    Test loading seafloor_curst_age with incorrect registration type.
    """
    with pytest.raises(GMTInvalidInput):
        load_seafloor_crust_age(registration="improper_type")


def test_seafloor_crust_age_01d():
    """
    Test some properties of the seafloor crust age 01d data.
    """
    data = load_seafloor_crust_age(resolution="01d", registration="gridline")
    assert data.shape == (181, 361)
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), 0.167381, rtol=1e-5)
    npt.assert_allclose(data.max(), 338.0274, rtol=1e-5)


def test_seafloor_crust_age_01d_with_region():
    """
    Test loading low-resolution seafloor crust age with 'region'.
    """
    data = load_seafloor_crust_age(
        resolution="01d", region=[-10, 10, -5, 5], registration="gridline"
    )
    assert data.shape == (11, 21)
    npt.assert_allclose(data.lat, np.arange(-5, 6, 1))
    npt.assert_allclose(data.lon, np.arange(-10, 11, 1))
    npt.assert_allclose(data.min(), 11.293945)
    npt.assert_allclose(data.max(), 125.1189)


def test_seafloor_crust_age_30m():
    """
    Test properties of the seafloor crust age 30m data.
    """
    data = load_seafloor_crust_age(resolution="30m", registration="gridline")
    assert data.shape == (361, 721)
    npt.assert_allclose(data.lat, np.arange(-90, 90.5, 0.5))
    npt.assert_allclose(data.lon, np.arange(-180, 180.5, 0.5))
    npt.assert_allclose(data.min(), 0.079903, rtol=1e-5)
    npt.assert_allclose(data.max(), 338.68396, rtol=1e-5)


def test_seafloor_crust_age_05m_with_region():
    """
    Test loading a subregion of high-resolution seafloor crust age.
    """
    data = load_seafloor_crust_age(
        resolution="05m", region=[-50, -40, 20, 30], registration="gridline"
    )
    assert data.coords["lat"].data.min() == 20.0
    assert data.coords["lat"].data.max() == 30.0
    assert data.coords["lon"].data.min() == -50.0
    assert data.coords["lon"].data.max() == -40.0
    npt.assert_allclose(data.data.min(), 0.040000916)
    npt.assert_allclose(data.data.max(), 46.530003)
    assert data.sizes["lat"] == 121
    assert data.sizes["lon"] == 121


def test_seafloor_crust_age_05m_without_region():
    """
    Test loading high-resolution seafloor crust age without passing 'region'.
    """
    with pytest.raises(GMTInvalidInput):
        load_seafloor_crust_age("05m")
