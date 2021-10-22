"""
Tests for surface.
"""
import os

import pandas as pd
import pytest
import xarray as xr
from numpy import testing as npt
from pygmt import surface, which
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile, data_kind


@pytest.fixture(scope="module", name="fname")
def fixture_fname():
    """
    Load the sample data remote file path.
    """
    return which("@Table_5_11.txt", download="c")


@pytest.fixture(scope="module", name="data")
def fixture_data(fname):
    """
    Load Table 5.11 in Davis: Statistics and Data Analysis in Geology.
    """
    return pd.read_csv(fname, sep=r"\s+", header=None, names=["x", "y", "z"])


@pytest.fixture(scope="module", name="region")
def fixture_region():
    """
    Define the data region.
    """
    return [-0.2, 6.6, -0.2, 6.2]


def check_values(grid):
    """
    Check the attributes and values of the DataArray returned by surface.
    """
    assert isinstance(grid, xr.DataArray)
    assert grid.gmt.registration == 0  # Gridline registration
    assert grid.gmt.gtype == 0  # Cartesian type
    assert grid.coords["y"].data.min() == -0.2
    assert grid.coords["y"].data.max() == 6.2
    assert grid.coords["x"].data.min() == -0.2
    assert grid.coords["x"].data.max() == 6.6
    npt.assert_allclose(grid[0, 0].values, 1011.1221)
    assert grid.sizes["y"] == 33
    assert grid.sizes["x"] == 35


def test_surface_input_file(fname, region):
    """
    Run surface by passing in a filename.
    """
    output = surface(data=fname, spacing="0.2", region=region)
    check_values(output)


def test_surface_input_data_array(data, region):
    """
    Run surface by passing in a numpy array into data.
    """
    data = data.values  # convert pandas.DataFrame to numpy.ndarray
    output = surface(data=data, spacing="0.2", region=region)
    check_values(output)


def test_surface_input_xyz(data, region):
    """
    Run surface by passing in x, y, z numpy.ndarrays individually.
    """
    output = surface(
        x=data.x,
        y=data.y,
        z=data.z,
        spacing="0.2",
        region=region,
    )
    check_values(output)


def test_surface_wrong_kind_of_input(data, region):
    """
    Run surface using grid input that is not file/matrix/vectors.
    """
    data = data.z.to_xarray()  # convert pandas.Series to xarray.DataArray
    assert data_kind(data) == "grid"
    with pytest.raises(GMTInvalidInput):
        surface(data=data, spacing="0.2", region=region)


def test_surface_with_outgrid_param(data, region):
    """
    Run surface with the -Goutputfile.nc parameter.
    """
    data = data.values  # convert pandas.DataFrame to numpy.ndarray
    with GMTTempFile(suffix=".nc") as tmpfile:
        output = surface(data=data, spacing="0.2", region=region, outgrid=tmpfile.name)
        assert output is None  # check that output is None since outgrid is set
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists at path
        with xr.open_dataarray(tmpfile.name) as grid:
            check_values(grid)


def test_surface_deprecate_outfile_to_outgrid(data, region):
    """
    Make sure that the old parameter "outfile" is supported and it reports a
    warning.
    """
    with pytest.warns(expected_warning=FutureWarning) as record:
        data = data.values  # convert pandas.DataFrame to numpy.ndarray
        with GMTTempFile(suffix=".nc") as tmpfile:
            output = surface(
                data=data, spacing="0.2", region=region, outfile=tmpfile.name
            )
            assert output is None  # check that output is None since outfile is set
            assert os.path.exists(path=tmpfile.name)  # check that file exists at path
            with xr.open_dataarray(tmpfile.name) as grid:
                check_values(grid)
        assert len(record) == 1  # check that only one warning was raised
