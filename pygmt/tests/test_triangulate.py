"""
Tests for triangulate
"""
import os

import pandas as pd
import pytest
import xarray as xr

from .. import triangulate, which
from ..datasets import load_sample_bathymetry
from ..exceptions import GMTInvalidInput
from ..helpers import data_kind

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TEMP_GRID = os.path.join(TEST_DATA_DIR, "tmp_grid.nc")


@pytest.fixture(scope="module", name="ship_data")
def fixture_ship_data():
    """
    Load the grid data from the sample bathymetry file
    """
    ship_data = load_sample_bathymetry()
    return ship_data


def test_triangulate_input_file():
    """
    Run triangulate by passing in a filename
    """
    fname = which("@tut_ship.xyz", download="c")
    output = triangulate(data=fname)
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (161935, 3)
    return output


def test_triangulate_input_data_array(ship_data):
    """
    Run triangulate by passing in a numpy array into data
    """
    data = ship_data.to_numpy()
    output = triangulate(data=data)
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (161935, 3)
    return output


def test_triangulate_input_xyz(ship_data):
    """
    Run triangulate by passing in x, y, z numpy.ndarrays individually
    """
    output = triangulate(
        x=ship_data.longitude,
        y=ship_data.latitude,
        z=ship_data.bathymetry,
    )
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (161935, 3)
    return output


def test_triangulate_input_xy_no_z(ship_data):
    """
    Run triangulate by passing in x and y, but no z
    """
    with pytest.raises(GMTInvalidInput):
        triangulate(x=ship_data.longitude, y=ship_data.latitude)


def test_triangulate_wrong_kind_of_input(ship_data):
    """
    Run triangulate using grid input that is not file/matrix/vectors
    """
    data = ship_data.bathymetry.to_xarray()  # convert pandas.Series to xarray.DataArray
    assert data_kind(data) == "grid"
    with pytest.raises(GMTInvalidInput):
        triangulate(data=data)


def test_triangulate_with_outgrid_true(ship_data):
    """
    Run triangulate with outgrid=True and see it load into an xarray.DataArray
    """
    data = ship_data.to_numpy()
    output = triangulate(
        data=data, spacing="5m", region=[245, 255, 20, 30], outgrid=True
    )
    assert isinstance(output, xr.DataArray)
    assert output.shape == (121, 121)
    return output


def test_triangulate_with_outgrid_param(ship_data):
    """
    Run triangulate with the -Goutputfile.nc parameter
    """
    data = ship_data.to_numpy()
    try:
        output = triangulate(
            data=data, spacing="5m", region=[245, 255, 20, 30], outgrid=TEMP_GRID
        )
        assert output is None  # check that output is None since outgrid is set
        assert os.path.exists(path=TEMP_GRID)  # check that outgrid exists at path
        with xr.open_dataarray(TEMP_GRID) as grid:
            assert isinstance(grid, xr.DataArray)  # ensure netcdf grid loads ok
            assert grid.shape == (121, 121)
    finally:
        os.remove(path=TEMP_GRID)
    return output


def test_triangulate_short_aliases(ship_data):
    """
    Run triangulate using short aliases -I for spacing, -R for region, -G for
    outgrid
    """
    data = ship_data.to_numpy()
    try:
        output = triangulate(data=data, I="5m", R=[245, 255, 20, 30], G=TEMP_GRID)
        assert output is None  # check that output is None since outgrid is set
        assert os.path.exists(path=TEMP_GRID)  # check that outgrid exists at path
        with xr.open_dataarray(TEMP_GRID) as grid:
            assert isinstance(grid, xr.DataArray)  # ensure netcdf grid loads ok
    finally:
        os.remove(path=TEMP_GRID)
    return output
