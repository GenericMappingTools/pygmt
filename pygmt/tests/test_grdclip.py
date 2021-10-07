"""
Tests for grdclip.
"""
import os

import pytest
import xarray as xr
from pygmt import grdclip, load_dataarray
from pygmt.datasets import load_earth_relief
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(resolution="01d", region=[-5, 5, -5, 5])


@pytest.fixture(scope="module", name="expected_grid")
def fixture_grid_result():
    """
    Load the expected grdclip grid result.
    """
    return xr.DataArray(
        data=[
            [-1800.0, -1800.0, -1800.0, -1800.0],
            [-1800.0, -1800.0, -1800.0, -1800.0],
            [-656.0, 40.0, -1800.0, -1800.0],
        ],
        coords=dict(lon=[-2.5, -1.5, -0.5, 0.5], lat=[2.5, 3.5, 4.5]),
        dims=["lat", "lon"],
    )


def test_grdclip_outgrid(grid, expected_grid):
    """
    Test the below and above parameters for grdclip and creates a test outgrid.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdclip(
            grid=grid,
            outgrid=tmpfile.name,
            below=[-1500, -1800],
            above=[-200, 40],
            region=[-3, 1, 2, 5],
        )
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        temp_grid = load_dataarray(tmpfile.name)
        assert temp_grid.dims == ("lat", "lon")
        assert temp_grid.gmt.gtype == 1  # Geographic grid
        assert temp_grid.gmt.registration == 1  # Pixel registration
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdclip_no_outgrid(grid, expected_grid):
    """
    Test the below and above parameters for grdclip with no set outgrid.
    """
    temp_grid = grdclip(
        grid=grid, below=[-1500, -1800], above=[-200, 40], region=[-3, 1, 2, 5]
    )
    assert temp_grid.dims == ("lat", "lon")
    assert temp_grid.gmt.gtype == 1  # Geographic grid
    assert temp_grid.gmt.registration == 1  # Pixel registration
    xr.testing.assert_allclose(a=temp_grid, b=expected_grid)
