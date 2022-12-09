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
    assert data["year"].min() == 1987
    assert data["year"].max() == 1988
    assert data["month"].min() == 1
    assert data["month"].max() == 12
    assert data["day"].min() == 1
    assert data["day"].max() == 31


def test_load_sample_data():
    """
    Check that the dataset loads without errors.
    """
    data = load_sample_data(name="japan_quakes")
    assert data.shape == (115, 7)
    assert data["year"].min() == 1987
    assert data["year"].max() == 1988
    assert data["month"].min() == 1
    assert data["month"].max() == 12
    assert data["day"].min() == 1
    assert data["day"].max() == 31


def test_ocean_ridge_points():
    """
    Check that the @ridge.txt dataset loads without errors.
    """
    with pytest.warns(expected_warning=FutureWarning) as record:
        data = load_ocean_ridge_points()
        assert len(record) == 1
    assert data.shape == (4146, 2)
    assert data["longitude"].min() == -179.9401
    assert data["longitude"].max() == 179.935
    assert data["latitude"].min() == -65.6182
    assert data["latitude"].max() == 86.8


def test_sample_bathymetry():
    """
    Check that the @tut_ship.xyz dataset loads without errors.
    """
    with pytest.warns(expected_warning=FutureWarning) as record:
        data = load_sample_bathymetry()
        assert len(record) == 1
    assert data.shape == (82970, 3)
    assert data["longitude"].min() == 245.0
    assert data["longitude"].max() == 254.705
    assert data["latitude"].min() == 20.0
    assert data["latitude"].max() == 29.99131
    assert data["bathymetry"].min() == -7708.0
    assert data["bathymetry"].max() == -9.0


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
    assert data["length"].min() == 98.6561
    assert data["length"].max() == 984.652
    assert data["azimuth"].min() == 0.0
    assert data["azimuth"].max() == 360.0


def test_mars_shape():
    """
    Check that the @mars370d.txt dataset loads without errors.
    """
    with pytest.warns(expected_warning=FutureWarning) as record:
        data = load_mars_shape()
        assert len(record) == 1
    assert data.shape == (370, 3)
    assert data["longitude"].min() == 0.008
    assert data["longitude"].max() == 359.983
    assert data["latitude"].min() == -79.715
    assert data["latitude"].max() == 85.887
    assert data["radius(m)"].min() == -6930
    assert data["radius(m)"].max() == 15001


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
    assert data["x"].min() == 0.2
    assert data["x"].max() == 6.3
    assert data["y"].min() == 0
    assert data["y"].max() == 6.2
    assert data["z"].min() == 690
    assert data["z"].max() == 960


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
    assert data["date"].min() == 1958.2027
    assert data["date"].max() == 2019.3699
    assert data["co2_ppm"].min() == 313.2
    assert data["co2_ppm"].max() == 414.83


def test_rock_sample_compositions():
    """
    Check that the @ternary.txt dataset loads without errors.
    """
    data = load_sample_data(name="rock_compositions")
    assert data.shape == (1000, 4)
    assert data["limestone"].min() == 0
    assert data["limestone"].max() == 1
    assert data["water"].min() == 0
    assert data["water"].max() == 0.921
    assert data["air"].min() == 0
    assert data["air"].max() == 0.981
    assert data["permittivity"].min() == 1.041
    assert data["permittivity"].max() == 70.844
