"""
Test pygmt.grdpaste.
"""

import xarray as xr
from pygmt import grdcut, grdpaste
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import load_static_earth_relief


def test_grdpaste():
    """
    Test grdpaste by pasting two grids together along their common edge.
    """
    grid = load_static_earth_relief()

    # Cut the grid into two non-overlapping parts
    grid_top = grdcut(grid, region=[-53, -49, -19, -16])
    grid_bottom = grdcut(grid, region=[-53, -49, -22, -19])

    # Paste the two grids back together
    result = grdpaste(grid_a=grid_top, grid_b=grid_bottom)

    # Check that the result is a DataArray
    assert isinstance(result, xr.DataArray)

    # Check that the result has the expected shape
    # grid_top has 3x4, grid_bottom has 3x4, so result should have 6x4
    assert result.shape == (6, 4)


def test_grdpaste_outgrid():
    """
    Test grdpaste with outgrid parameter.
    """
    grid = load_static_earth_relief()

    # Cut the grid into two non-overlapping parts
    grid_top = grdcut(grid, region=[-53, -49, -19, -16])
    grid_bottom = grdcut(grid, region=[-53, -49, -22, -19])

    # Paste the two grids back together and save to file
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdpaste(grid_a=grid_top, grid_b=grid_bottom, outgrid=tmpfile.name)
        assert result is None  # grdpaste returns None if output to a file
        temp_grid = xr.load_dataarray(tmpfile.name, engine="gmt", raster_kind="grid")
        assert isinstance(temp_grid, xr.DataArray)
        assert temp_grid.shape == (6, 4)


def test_grdpaste_edgeinfo():
    """
    Test grdpaste with edgeinfo parameter.
    """
    grid = load_static_earth_relief()

    # Cut the grid into two non-overlapping parts
    grid_top = grdcut(grid, region=[-53, -49, -19, -16])
    grid_bottom = grdcut(grid, region=[-53, -49, -22, -19])

    # Get edge information without pasting
    result = grdpaste(grid_a=grid_top, grid_b=grid_bottom, edgeinfo=True)
    # Should return a string with edge information
    assert isinstance(result, str)
    assert len(result) > 0


def test_grdpaste_coltypes():
    """
    Test grdpaste with coltypes parameter.
    """
    grid = load_static_earth_relief()

    # Cut the grid into two non-overlapping parts
    grid_top = grdcut(grid, region=[-53, -49, -19, -16])
    grid_bottom = grdcut(grid, region=[-53, -49, -22, -19])

    # Paste the two grids back together with coltypes="g" (geographic coordinates)
    result = grdpaste(grid_a=grid_top, grid_b=grid_bottom, coltypes="g")

    # Check that the result is a DataArray
    assert isinstance(result, xr.DataArray)

    # Check that the result has the expected shape
    # grid_top has 3x4, grid_bottom has 3x4, so result should have 6x4
    assert result.shape == (6, 4)
