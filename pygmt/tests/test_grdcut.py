"""
Tests for grdcut.
"""
import os

import numpy as np
import pytest
import xarray as xr
from pygmt import grdcut, load_dataarray
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(registration="pixel")


@pytest.fixture(scope="module", name="expected_grid")
def fixture_grid_result():
    """
    Load the expected grdcut grid result.
    """
    return xr.DataArray(
        data=[
            [-5069.5, -5105.0, -4937.0, -4708.0],
            [-4115.5, -4996.0, -4762.0, -4599.0],
            [-656.0, -160.0, -3484.5, -3897.5],
        ],
        coords=dict(lon=[-2.5, -1.5, -0.5, 0.5], lat=[2.5, 3.5, 4.5]),
        dims=["lat", "lon"],
    )


def test_grdcut_file_in_file_out(expected_grid):
    """
    grdcut an input grid file, and output to a grid file.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdcut("@earth_relief_01d", outgrid=tmpfile.name, region=[-3, 1, 2, 5])
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdcut_file_in_dataarray_out(expected_grid):
    """
    grdcut an input grid file, and output as DataArray.
    """
    outgrid = grdcut("@earth_relief_01d", region=[-3, 1, 2, 5])
    assert isinstance(outgrid, xr.DataArray)
    assert outgrid.gmt.registration == 1  # Pixel registration
    assert outgrid.gmt.gtype == 1  # Geographic type
    # check information of the output grid
    xr.testing.assert_allclose(a=outgrid, b=expected_grid)


def test_grdcut_dataarray_in_file_out(grid, expected_grid):
    """
    grdcut an input DataArray, and output to a grid file.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdcut(grid, outgrid=tmpfile.name, region=[-3, 1, 2, 5])
        assert result is None  # grdcut returns None if output to a file
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdcut_dataarray_in_dataarray_out(grid, expected_grid):
    """
    grdcut an input DataArray, and output as DataArray.
    """
    outgrid = grdcut(grid, region=[-3, 1, 2, 5])
    assert isinstance(outgrid, xr.DataArray)
    xr.testing.assert_allclose(a=outgrid, b=expected_grid)


def test_grdcut_fails():
    """
    Check that grdcut fails correctly.
    """
    with pytest.raises(GMTInvalidInput):
        grdcut(np.arange(10).reshape((5, 2)))
