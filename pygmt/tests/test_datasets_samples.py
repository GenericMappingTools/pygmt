"""
Test basic functionality for loading sample datasets.
"""
import numpy.testing as npt
import pandas as pd
import pytest
from pygmt.datasets import (
    load_fractures_compilation,
    load_hotspots,
    load_japan_quakes,
    load_mars_shape,
    load_ocean_ridge_points,
    load_sample_bathymetry,
    load_sample_data,
    load_usgs_quakes,
)
from pygmt.exceptions import GMTInvalidInput


def test_load_sample_invalid():
    """
    Check that the function raises error for unsupported filenames.
    """
    with pytest.raises(GMTInvalidInput):
        load_sample_data(name="bad.filename")


def test_japan_quakes():
    """
    Check that the dataset loads without errors.
    """
    with pytest.warns(expected_warning=FutureWarning) as record:
        data = load_japan_quakes()
        assert len(record) == 1
    assert data.shape == (115, 7)
    summary = data.describe()
    assert summary.loc["min", "year"] == 1987
    assert summary.loc["max", "year"] == 1988
    assert summary.loc["min", "month"] == 1
    assert summary.loc["max", "month"] == 12
    assert summary.loc["min", "day"] == 1
    assert summary.loc["max", "day"] == 31


def test_load_sample_data():
    """
    Check that the dataset loads without errors.
    """
    data = load_sample_data(name="japan_quakes")
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
    with pytest.warns(expected_warning=FutureWarning) as record:
        data = load_ocean_ridge_points()
        assert len(record) == 1
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
    with pytest.warns(expected_warning=FutureWarning) as record:
        data = load_sample_bathymetry()
        assert len(record) == 1
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
    with pytest.warns(expected_warning=FutureWarning) as record:
        data = load_usgs_quakes()
        assert len(record) == 1
    assert data.shape == (1197, 22)


def test_fractures_compilation():
    """
    Check that the @fractures_06.txt dataset loads without errors.
    """
    with pytest.warns(expected_warning=FutureWarning) as record:
        data = load_fractures_compilation()
        assert len(record) == 1
    assert data.shape == (361, 2)
    summary = data.describe()
    assert summary.loc["min", "length"] == 98.6561
    assert summary.loc["max", "length"] == 984.652
    assert summary.loc["min", "azimuth"] == 0.0
    assert summary.loc["max", "azimuth"] == 360.0


def test_mars_shape():
    """
    Check that the @mars370d.txt dataset loads without errors.
    """
    with pytest.warns(expected_warning=FutureWarning) as record:
        data = load_mars_shape()
        assert len(record) == 1
    assert data.shape == (370, 3)
    summary = data.describe()
    assert summary.loc["min", "longitude"] == 0.008
    assert summary.loc["max", "longitude"] == 359.983
    assert summary.loc["min", "latitude"] == -79.715
    assert summary.loc["max", "latitude"] == 85.887
    assert summary.loc["min", "radius(m)"] == -6930
    assert summary.loc["max", "radius(m)"] == 15001


def test_hotspots():
    """
    Check that the @hotspots.txt dataset loads without errors.
    """
    with pytest.warns(expected_warning=FutureWarning) as record:
        data = load_hotspots()
        assert len(record) == 1
    assert data.shape == (55, 4)
    assert list(data.columns) == [
        "longitude",
        "latitude",
        "symbol_size",
        "place_name",
    ]
    assert isinstance(data, pd.DataFrame)


def test_load_notre_dame_topography():
    """
    Check that the @Table_5_11.txt dataset loads without errors.
    """
    data = load_sample_data(name="notre_dame_topography")
    assert data.shape == (52, 3)
    summary = data.describe()
    assert summary.loc["min", "x"] == 0.2
    assert summary.loc["max", "x"] == 6.3
    assert summary.loc["min", "y"] == 0
    assert summary.loc["max", "y"] == 6.2
    assert summary.loc["min", "z"] == 690
    assert summary.loc["max", "z"] == 960


def test_earth_relief_holes():
    """
    Check that the @earth_relief_20m_holes.grd dataset loads without errors.
    """
    grid = load_sample_data(name="earth_relief_holes")
    assert grid.shape == (31, 31)
    npt.assert_allclose(grid.max(), 1601)
    npt.assert_allclose(grid.min(), -4929.5)
    # Test for the NaN values in the remote file
    assert grid[2, 21].isnull()


def test_maunaloa_co2():
    """
    Check that the @MaunaLoa_CO2.txt dataset loads without errors.
    """
    data = load_sample_data(name="maunaloa_co2")
    assert data.shape == (730, 2)
    summary = data.describe()
    assert summary.loc["min", "date"] == 1958.2027
    assert summary.loc["max", "date"] == 2019.3699
    assert summary.loc["min", "co2_ppm"] == 313.2
    assert summary.loc["max", "co2_ppm"] == 414.83
