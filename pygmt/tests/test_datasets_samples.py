"""
Test basic functionality for loading sample datasets.
"""
from pygmt.datasets import (
    load_fractures_compilation,
    load_japan_quakes,
    load_ocean_ridge_points,
    load_sample_bathymetry,
    load_usgs_quakes,
)


def test_japan_quakes():
    """
    Check that the dataset loads without errors.
    """
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
    """
    Check that the @ridge.txt dataset loads without errors.
    """
    data = load_ocean_ridge_points()
    assert data.shape == (4146, 2)
    summary = data.describe()
    assert summary.loc["min", "longitude"] == -179.9401
    assert summary.loc["max", "longitude"] == 179.935
    assert summary.loc["min", "latitude"] == -65.6182
    assert summary.loc["max", "latitude"] == 86.8


def test_sample_bathymetry():
    """
    Check that the @tut_ship.xyz dataset loads without errors.
    """
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
    """
    Check that the dataset loads without errors.
    """
    data = load_usgs_quakes()
    assert data.shape == (1197, 22)


def test_fractures_compilation():
    """
    Check that the @fractures_06.txt dataset loads without errors.
    """
    data = load_fractures_compilation()
    assert data.shape == (361, 2)
    summary = data.describe()
    assert summary.loc["min", "length"] == 98.6561
    assert summary.loc["max", "length"] == 984.652
    assert summary.loc["min", "azimuth"] == 0.0
    assert summary.loc["max", "azimuth"] == 360.0
