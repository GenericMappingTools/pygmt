"""
Tests for surface.
"""
import os

import pytest
import xarray as xr
from pygmt import surface, which
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


def test_surface_input_file():
    """
    Run surface by passing in a filename.
    """
    fname = which("@tut_ship.xyz", download="c")
    output = surface(data=fname, spacing="5m", region=[245, 255, 20, 30])
    assert isinstance(output, xr.DataArray)
    assert output.gmt.registration == 0  # Gridline registration
    assert output.gmt.gtype == 0  # Cartesian type


def test_surface_input_data_array(ship_data):
    """
    Run surface by passing in a numpy array into data.
    """
    data = ship_data.values  # convert pandas.DataFrame to numpy.ndarray
    output = surface(data=data, spacing="5m", region=[245, 255, 20, 30])
    assert isinstance(output, xr.DataArray)


def test_surface_input_xyz(ship_data):
    """
    Run surface by passing in x, y, z numpy.ndarrays individually.
    """
    output = surface(
        x=ship_data.longitude,
        y=ship_data.latitude,
        z=ship_data.bathymetry,
        spacing="5m",
        region=[245, 255, 20, 30],
    )
    assert isinstance(output, xr.DataArray)


def test_surface_wrong_kind_of_input(ship_data):
    """
    Run surface using grid input that is not file/matrix/vectors.
    """
    data = ship_data.bathymetry.to_xarray()  # convert pandas.Series to xarray.DataArray
    assert data_kind(data) == "grid"
    with pytest.raises(GMTInvalidInput):
        surface(data=data, spacing="5m", region=[245, 255, 20, 30])


def test_surface_with_outgrid_param(ship_data):
    """
    Run surface with the -Goutputfile.nc parameter.
    """
    data = ship_data.values  # convert pandas.DataFrame to numpy.ndarray
    try:
        output = surface(
            data=data, spacing="5m", region=[245, 255, 20, 30], outgrid=TEMP_GRID
        )
        assert output is None  # check that output is None since outgrid is set
        assert os.path.exists(path=TEMP_GRID)  # check that outgrid exists at path
        with xr.open_dataarray(TEMP_GRID) as grid:
            assert isinstance(grid, xr.DataArray)  # ensure netcdf grid loads ok
    finally:
        os.remove(path=TEMP_GRID)


def test_surface_deprecate_outfile_to_outgrid(ship_data):
    """
    Make sure that the old parameter "outfile" is supported and it reports a
    warning.
    """
    with pytest.warns(expected_warning=FutureWarning) as record:
        data = ship_data.values  # convert pandas.DataFrame to numpy.ndarray
        try:
            output = surface(
                data=data, spacing="5m", region=[245, 255, 20, 30], outfile=TEMP_GRID
            )
            assert output is None  # check that output is None since outfile is set
            assert os.path.exists(path=TEMP_GRID)  # check that file exists at path

            with xr.open_dataarray(TEMP_GRID) as grid:
                assert isinstance(grid, xr.DataArray)  # ensure netcdf grid loads ok
        finally:
            os.remove(path=TEMP_GRID)
        assert len(record) == 1  # check that only one warning was raised


def test_surface_short_aliases(ship_data):
    """
    Run surface using short aliases -I for spacing, -R for region, -G for
    outgrid.
    """
    data = ship_data.values  # convert pandas.DataFrame to numpy.ndarray
    try:
        output = surface(data=data, I="5m", R=[245, 255, 20, 30], G=TEMP_GRID)
        assert output is None  # check that output is None since outgrid is set
        assert os.path.exists(path=TEMP_GRID)  # check that outgrid exists at path
        with xr.open_dataarray(TEMP_GRID) as grid:
            assert isinstance(grid, xr.DataArray)  # ensure netcdf grid loads ok
    finally:
        os.remove(path=TEMP_GRID)
