"""
Tests for triangulate.
"""
import os

import pandas as pd
import pytest
import xarray as xr
from pygmt import triangulate
from pygmt.datasets import load_sample_bathymetry
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile, data_kind


@pytest.fixture(scope="module", name="dataframe")
def fixture_dataframe():
    """
    Load the table data from the sample bathymetry dataset.
    """
    return load_sample_bathymetry()


def test_triangulate_input_file():
    """
    Run triangulate by passing in a filename.
    """
    output = triangulate(data="@tut_ship.xyz")
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (161935, 3)


def test_triangulate_input_data_array(dataframe):
    """
    Run triangulate by passing in a numpy array into data.
    """
    data = dataframe.to_numpy()
    output = triangulate(data=data)
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (161935, 3)


def test_triangulate_input_xyz(dataframe):
    """
    Run triangulate by passing in x, y, z numpy.ndarrays individually.
    """
    output = triangulate(
        x=dataframe.longitude,
        y=dataframe.latitude,
        z=dataframe.bathymetry,
    )
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (161935, 3)


def test_triangulate_input_xy_no_z(dataframe):
    """
    Run triangulate by passing in x and y, but no z.
    """
    output = triangulate(x=dataframe.longitude, y=dataframe.latitude)
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (161935, 3)


def test_triangulate_wrong_kind_of_input(dataframe):
    """
    Run triangulate using grid input that is not file/matrix/vectors.
    """
    data = dataframe.bathymetry.to_xarray()  # convert pandas.Series to xarray.DataArray
    assert data_kind(data) == "grid"
    with pytest.raises(GMTInvalidInput):
        triangulate(data=data)


def test_triangulate_with_outgrid_true(dataframe):
    """
    Run triangulate with outgrid=True and see it load into an xarray.DataArray.
    """
    data = dataframe.to_numpy()
    output = triangulate(
        data=data, spacing="5m", region=[245, 255, 20, 30], outgrid=True
    )
    assert isinstance(output, xr.DataArray)
    assert output.shape == (121, 121)


def test_triangulate_with_outgrid_param(dataframe):
    """
    Run triangulate with the -Goutputfile.nc parameter.
    """
    data = dataframe.to_numpy()
    with GMTTempFile(suffix=".nc") as tmpfile:
        output = triangulate(
            data=data, spacing="5m", region=[245, 255, 20, 30], outgrid=tmpfile.name
        )
        assert output is None  # check that output is None since outgrid is set
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        with xr.open_dataarray(tmpfile.name) as grid:
            assert isinstance(grid, xr.DataArray)  # ensure netcdf grid loads ok
            assert grid.shape == (121, 121)
