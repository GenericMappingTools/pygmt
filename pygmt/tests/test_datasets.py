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
    resolutions = "1m 1d bla 60d 01s 03s 001m 03".split()
    resolutions.append(60)
    for resolution in resolutions:
        with pytest.raises(GMTInvalidInput):
            load_earth_relief(resolution=resolution)


# Only test 60m and 30m to avoid downloading large datasets in CI
def test_earth_relief_60():
    "Test some properties of the earth relief 60m data"
    data = load_earth_relief(resolution="60m")
    assert data.shape == (181, 361)
    npt.assert_allclose(data.lat, np.arange(-90, 91, 1))
    npt.assert_allclose(data.lon, np.arange(-180, 181, 1))
    npt.assert_allclose(data.min(), -8592)
    npt.assert_allclose(data.max(), 5559)


def test_earth_relief_30():
    "Test some properties of the earth relief 30m data"
    data = load_earth_relief(resolution="30m")
    assert data.shape == (361, 721)
    npt.assert_allclose(data.lat, np.arange(-90, 90.5, 0.5))
    npt.assert_allclose(data.lon, np.arange(-180, 180.5, 0.5))
    npt.assert_allclose(data.min(), -9460)
    npt.assert_allclose(data.max(), 5888)
