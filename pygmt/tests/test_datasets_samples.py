"""
Test basic functionality for loading sample datasets.
"""
import numpy.testing as npt
import pandas as pd
import pytest
from pygmt.datasets import load_sample_data
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
    data = load_sample_data(name="ocean_ridge_points")
    assert data.shape == (4146, 2)
    assert data["longitude"].min() == -179.9401
    assert data["longitude"].max() == 179.935
    assert data["latitude"].min() == -65.6182
    assert data["latitude"].max() == 86.8


def test_sample_bathymetry():
    """
    Check that the @tut_ship.xyz dataset loads without errors.
    """
    data = load_sample_data(name="bathymetry")
    assert data.shape == (82970, 3)
    assert data["longitude"].min() == 245.0
    assert data["longitude"].max() == 254.705
    assert data["latitude"].min() == 20.0
    assert data["latitude"].max() == 29.99131
    assert data["bathymetry"].min() == -7708.0
    assert data["bathymetry"].max() == -9.0


def test_usgs_quakes():
    """
    Check that the @usgs_quakes_22.txt dataset loads without errors.
    """
    data = load_sample_data(name="usgs_quakes")
    assert data.shape == (1197, 22)
    assert list(data.columns) == [
        "time",
        "latitude",
        "longitude",
        "depth",
        "mag",
        "magType",
        "nst",
        "gap",
        "dmin",
        "rms",
        "net",
        "id",
        "updated",
        "place",
        "type",
        "horizontalError",
        "depthError",
        "magError",
        "magNst",
        "status",
        "locationSource",
        "magSource",
    ]
    npt.assert_allclose(data["latitude"].min(), -60.6819)
    npt.assert_allclose(data["latitude"].max(), 72.6309)
    npt.assert_allclose(data["longitude"].min(), -179.9953)
    npt.assert_allclose(data["longitude"].max(), 179.9129)
    npt.assert_allclose(data["depth"].min(), -0.21)
    npt.assert_allclose(data["depth"].max(), 640.49)
    npt.assert_allclose(data["mag"].min(), 3)
    npt.assert_allclose(data["mag"].max(), 8.1)
    npt.assert_allclose(data["nst"].min(), 3)
    npt.assert_allclose(data["nst"].max(), 167)
    npt.assert_allclose(data["gap"].min(), 10.0)
    npt.assert_allclose(data["gap"].max(), 353.0)
    npt.assert_allclose(data["dmin"].min(), 0.006421)
    npt.assert_allclose(data["dmin"].max(), 39.455)
    npt.assert_allclose(data["rms"].min(), 0.02)
    npt.assert_allclose(data["rms"].max(), 1.76)
    npt.assert_allclose(data["horizontalError"].min(), 0.09)
    npt.assert_allclose(data["horizontalError"].max(), 36.8)
    npt.assert_allclose(data["depthError"].min(), 0)
    npt.assert_allclose(data["depthError"].max(), 65.06)
    npt.assert_allclose(data["magError"].min(), 0.02)
    npt.assert_allclose(data["magError"].max(), 0.524)
    npt.assert_allclose(data["magNst"].min(), 1)
    npt.assert_allclose(data["magNst"].max(), 944)


def test_fractures_compilation():
    """
    Check that the @fractures_06.txt dataset loads without errors.
    """
    data = load_sample_data(name="fractures")
    assert data.shape == (361, 2)
    assert data["length"].min() == 98.6561
    assert data["length"].max() == 984.652
    assert data["azimuth"].min() == 0.0
    assert data["azimuth"].max() == 360.0


def test_mars_shape():
    """
    Check that the @mars370d.txt dataset loads without errors.
    """
    data = load_sample_data(name="mars_shape")
    assert data.shape == (370, 3)
    assert data["longitude"].min() == 0.008
    assert data["longitude"].max() == 359.983
    assert data["latitude"].min() == -79.715
    assert data["latitude"].max() == 85.887
    assert data["radius_m"].min() == -6930
    assert data["radius_m"].max() == 15001


def test_hotspots():
    """
    Check that the @hotspots.txt dataset loads without errors.
    """
    data = load_sample_data(name="hotspots")
    assert data.shape == (55, 4)
    assert list(data.columns) == [
        "longitude",
        "latitude",
        "symbol_size",
        "place_name",
    ]
    assert isinstance(data, pd.DataFrame)
    assert data["longitude"].min() == -169.6
    assert data["longitude"].max() == 167
    assert data["latitude"].min() == -78
    assert data["latitude"].max() == 64
    assert data["symbol_size"].min() == 0.25
    assert data["symbol_size"].max() == 0.5


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
