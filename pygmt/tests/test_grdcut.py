"""
Tests for grdcut.
"""
import numpy as np
import pytest
import xarray as xr
from pygmt import grdcut, load_dataarray
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import load_static_earth_relief


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_static_earth_relief()


@pytest.fixture(scope="module", name="region")
def fixture_region():
    """
    Set the data region.
    """
    return [-53, -49, -20, -17]


@pytest.fixture(scope="module", name="expected_grid")
def fixture_expected_grid():
    """
    Load the expected grdcut grid result.
    """
    return xr.DataArray(
        data=[
            [446.5, 481.5, 439.5, 553.0],
            [757.0, 570.5, 538.5, 524.0],
            [796.0, 886.0, 571.5, 638.5],
        ],
        coords=dict(lon=[-52.5, -51.5, -50.5, -49.5], lat=[-19.5, -18.5, -17.5]),
        dims=["lat", "lon"],
    )


def test_grdcut_dataarray_in_file_out(grid, expected_grid, region):
    """
    grdcut an input DataArray, and output to a grid file.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdcut(grid, outgrid=tmpfile.name, region=region)
        assert result is None  # grdcut returns None if output to a file
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdcut_dataarray_in_dataarray_out(grid, expected_grid, region):
    """
    grdcut an input DataArray, and output as DataArray.
    """
    outgrid = grdcut(grid, region=region)
    assert isinstance(outgrid, xr.DataArray)
    xr.testing.assert_allclose(a=outgrid, b=expected_grid)


def test_grdcut_fails():
    """
    Check that grdcut fails correctly.
    """
    with pytest.raises(GMTInvalidInput):
        grdcut(np.arange(10).reshape((5, 2)))
