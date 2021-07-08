"""
Tests for nearneighbor.
"""
import os

import pytest
import xarray as xr
from pygmt import nearneighbor, which
from pygmt.datasets import load_sample_bathymetry
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import data_kind

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TEMP_GRID = os.path.join(TEST_DATA_DIR, "tmp_grid.nc")


@pytest.fixture(scope="module", name="ship_data")
def fixture_ship_data():
    """
    Load the data from the sample bathymetry dataset.
    """
    return load_sample_bathymetry()


def test_nearneighbor_input_file():
    """
    Run nearneighbor by passing in a filename.
    """
    fname = which("@tut_ship.xyz", download="c")
    output = nearneighbor(
        data=fname, spacing="5m", region=[245, 255, 20, 30], search_radius="10m"
    )
    assert isinstance(output, xr.DataArray)
    assert output.gmt.registration == 0  # Gridline registration
    assert output.gmt.gtype == 0  # Cartesian type
    return output


def test_nearneighbor_input_data_array(ship_data):
    """
    Run nearneighbor by passing in a numpy array into data.
    """
    data = ship_data.values  # convert pandas.DataFrame to numpy.ndarray
    output = nearneighbor(
        data=data, spacing="5m", region=[245, 255, 20, 30], search_radius="10m"
    )
    assert isinstance(output, xr.DataArray)
    return output


def test_nearneighbor_input_xyz(ship_data):
    """
    Run nearneighbor by passing in x, y, z numpy.ndarrays individually.
    """
    output = nearneighbor(
        x=ship_data.longitude,
        y=ship_data.latitude,
        z=ship_data.bathymetry,
        spacing="5m",
        region=[245, 255, 20, 30],
        search_radius="10m",
    )
    assert isinstance(output, xr.DataArray)
    return output


def test_nearneighbor_input_xy_no_z(ship_data):
    """
    Run nearneighbor by passing in x and y, but no z.
    """
    with pytest.raises(GMTInvalidInput):
        nearneighbor(
            x=ship_data.longitude,
            y=ship_data.latitude,
            spacing="5m",
            region=[245, 255, 20, 30],
            search_radius="10m",
        )


def test_nearneighbor_wrong_kind_of_input(ship_data):
    """
    Run nearneighbor using grid input that is not file/matrix/vectors.
    """
    data = ship_data.bathymetry.to_xarray()  # convert pandas.Series to xarray.DataArray
    assert data_kind(data) == "grid"
    with pytest.raises(GMTInvalidInput):
        nearneighbor(
            data=data, spacing="5m", region=[245, 255, 20, 30], search_radius="10m"
        )


def test_nearneighbor_with_outfile_param(ship_data):
    """
    Run nearneighbor with the -Goutputfile.nc parameter.
    """
    data = ship_data.values  # convert pandas.DataFrame to numpy.ndarray
    try:
        output = nearneighbor(
            data=data,
            spacing="5m",
            region=[245, 255, 20, 30],
            outfile=TEMP_GRID,
            search_radius="10m",
        )
        assert output is None  # check that output is None since outfile is set
        assert os.path.exists(path=TEMP_GRID)  # check that outfile exists at path
        with xr.open_dataarray(TEMP_GRID) as grid:
            assert isinstance(grid, xr.DataArray)  # ensure netcdf grid loads ok
    finally:
        os.remove(path=TEMP_GRID)
    return output


def test_nearneighbor_short_aliases(ship_data):
    """
    Run nearneighbor using short aliases -I for spacing, -R for region, -G for
    outfile, -S for search radius.
    """
    data = ship_data.values  # convert pandas.DataFrame to numpy.ndarray
    try:
        output = nearneighbor(
            data=data, I="5m", R=[245, 255, 20, 30], G=TEMP_GRID, S="10m"
        )
        assert output is None  # check that output is None since outfile is set
        assert os.path.exists(path=TEMP_GRID)  # check that outfile exists at path
        with xr.open_dataarray(TEMP_GRID) as grid:
            assert isinstance(grid, xr.DataArray)  # ensure netcdf grid loads ok
    finally:
        os.remove(path=TEMP_GRID)
    return output
