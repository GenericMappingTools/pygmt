"""
Tests for grdclip.
"""
from pathlib import Path

import pytest
import xarray as xr
from pygmt import grdclip, load_dataarray
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import load_static_earth_relief


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the static_earth_relief file.
    """
    return load_static_earth_relief()


@pytest.fixture(scope="module", name="expected_grid")
def fixture_expected_grid():
    """
    Load the expected grdclip grid result.
    """
    return xr.DataArray(
        data=[
            [1000.0, 570.5, -1000.0, -1000.0],
            [1000.0, 1000.0, 571.5, 638.5],
            [555.5, 556.0, 580.0, 1000.0],
        ],
        coords=dict(lon=[-52.5, -51.5, -50.5, -49.5], lat=[-18.5, -17.5, -16.5]),
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
            below=[550, -1000],
            above=[700, 1000],
            region=[-53, -49, -19, -16],
        )
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0  # check that outgrid exists
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
        grid=grid, below=[550, -1000], above=[700, 1000], region=[-53, -49, -19, -16]
    )
    assert temp_grid.dims == ("lat", "lon")
    assert temp_grid.gmt.gtype == 1  # Geographic grid
    assert temp_grid.gmt.registration == 1  # Pixel registration
    xr.testing.assert_allclose(a=temp_grid, b=expected_grid)
