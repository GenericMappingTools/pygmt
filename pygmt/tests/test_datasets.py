"""
Test basic functionality for loading datasets.
"""
import numpy as np
import numpy.testing as npt
import pytest

from ..datasets import (
    load_japan_quakes,
    load_earth_relief,
    load_ocean_ridge_points,
    load_sample_bathymetry,
    load_usgs_quakes,
)
from ..exceptions import GMTInvalidInput


def test_japan_quakes():
    "Check that the dataset loads without errors"
    data = load_japan_quakes()
    assert data.shape == (115, 7)
    summary = data.describe()
    assert summary.loc["min", "year"] == 1987
    assert summary.loc["max", "year"] == 1988
    assert summary.loc["min", "month"] == 1
    assert summary.loc["max", "month"] == 12
    assert summary.loc["min", "day"] == 1
    assert summary.loc["max", "day"] == 31


def test_ocean_ridge_points():
    "Check that the @ridge.txt dataset loads without errors"
    data = load_ocean_ridge_points()
    assert data.shape == (4146, 2)
    summary = data.describe()
    assert summary.loc["min", "longitude"] == -179.9401
    assert summary.loc["max", "longitude"] == 179.935
    assert summary.loc["min", "latitude"] == -65.6182
    assert summary.loc["max", "latitude"] == 86.8


def test_sample_bathymetry():
    "Check that the @tut_ship.xyz dataset loads without errors"
    data = load_sample_bathymetry()
    assert data.shape == (82970, 3)
    summary = data.describe()
    assert summary.loc["min", "longitude"] == 245.0
    assert summary.loc["max", "longitude"] == 254.705
    assert summary.loc["min", "latitude"] == 20.0
    assert summary.loc["max", "latitude"] == 29.99131
    assert summary.loc["min", "bathymetry"] == -7708.0
    assert summary.loc["max", "bathymetry"] == -9.0


def test_usgs_quakes():
    "Check that the dataset loads without errors"
    data = load_usgs_quakes()
    assert data.shape == (1197, 22)


def test_earth_relief_fails():
    "Make sure earth relief fails for invalid resolutions"
    resolutions = "1m 1d bla 60d 001m 03".split()
    resolutions.append(60)
    for resolution in resolutions:
        with pytest.raises(GMTInvalidInput):
            load_earth_relief(resolution=resolution)


# Only test 01d and 30m to avoid downloading large datasets in CI
def test_earth_relief_01d():
    "Test some properties of the earth relief 01d data"
    data = load_earth_relief(resolution="01d", registration="gridline")
    assert data.shape == (181, 361)
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -8592.5)
    npt.assert_allclose(data.max(), 5559.0)


def test_earth_relief_01d_with_region():
    "Test loading low-resolution earth relief with 'region'"
    with pytest.raises(NotImplementedError):
        load_earth_relief("01d", region=[0, 180, 0, 90])


def test_earth_relief_30m():
    "Test some properties of the earth relief 30m data"
    data = load_earth_relief(resolution="30m", registration="gridline")
    assert data.shape == (361, 721)
    npt.assert_allclose(data.lat, np.arange(-90, 90.5, 0.5))
    npt.assert_allclose(data.lon, np.arange(-180, 180.5, 0.5))
    npt.assert_allclose(data.min(), -9460.5)
    npt.assert_allclose(data.max(), 5887.5)


def test_earth_relief_05m_with_region():
    "Test loading a subregion of high-resolution earth relief grid"
    data = load_earth_relief(
        resolution="05m", region=[120, 160, 30, 60], registration="gridline"
    )
    assert data.coords["lat"].data.min() == 30.0
    assert data.coords["lat"].data.max() == 60.0
    assert data.coords["lon"].data.min() == 120.0
    assert data.coords["lon"].data.max() == 160.0
    assert data.data.min() == -9633.0
    assert data.data.max() == 2532.0
    assert data.sizes["lat"] == 361
    assert data.sizes["lon"] == 481


def test_earth_relief_05m_without_region():
    "Test loading high-resolution earth relief without passing 'region'"
    with pytest.raises(GMTInvalidInput):
        load_earth_relief("05m")


def test_earth_relief_incorrect_registration():
    "Test loading earth relief with incorrect registration type"
    with pytest.raises(GMTInvalidInput):
        load_earth_relief(registration="improper_type")
