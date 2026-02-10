"""
Test pygmt.grdpaste.
"""

import pytest
import xarray as xr
from pygmt import grdcut, grdpaste
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import load_static_earth_relief


@pytest.fixture(scope="module", name="grid_top")
def fixture_grid_top():
    """
    Load the top part of the grid data from the sample earth_relief file.
    """
    grid = load_static_earth_relief()
    return grdcut(grid, region=[-53, -49, -19, -16])


@pytest.fixture(scope="module", name="grid_bottom")
def fixture_grid_bottom():
    """
    Load the bottom part of the grid data from the sample earth_relief file.
    """
    grid = load_static_earth_relief()
    return grdcut(grid, region=[-53, -49, -22, -19])


def test_grdpaste(grid_top, grid_bottom):
    """
    Test grdpaste by pasting two grids together along their common edge.
    """
    # Paste the two grids back together
    result = grdpaste(grid1=grid_top, grid2=grid_bottom)

    # Check that the result is a DataArray
    assert isinstance(result, xr.DataArray)

    # Check that the result has the expected shape
    # grid_top has 3x4, grid_bottom has 3x4, so result should have 6x4
    assert result.shape == (6, 4)


def test_grdpaste_outgrid(grid_top, grid_bottom):
    """
    Test grdpaste with outgrid parameter.
    """
    # Paste the two grids back together and save to file
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdpaste(grid1=grid_top, grid2=grid_bottom, outgrid=tmpfile.name)
        assert result is None  # grdpaste returns None if output to a file
        temp_grid = xr.load_dataarray(tmpfile.name, engine="gmt", raster_kind="grid")
        assert isinstance(temp_grid, xr.DataArray)
        assert temp_grid.shape == (6, 4)
