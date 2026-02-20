"""
Test pygmt.grdpaste.
"""

import pytest
import xarray as xr
from packaging.version import Version
from pygmt import grdcut, grdpaste
from pygmt.clib import __gmt_version__
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import load_static_earth_relief


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_static_earth_relief()


@pytest.fixture(scope="module", name="grid_top")
def fixture_grid_top(grid):
    """
    Load the top part of the grid data from the sample earth_relief file.
    """
    return grdcut(grid, region=[-53, -49, -19, -16])


@pytest.fixture(scope="module", name="grid_bottom")
def fixture_grid_bottom(grid):
    """
    Load the bottom part of the grid data from the sample earth_relief file.
    """
    return grdcut(grid, region=[-53, -49, -22, -19])


def test_grdpaste_file_in_file_out(grid, grid_top, grid_bottom):
    """
    Test grdpaste with file input and file output.
    """
    with (
        GMTTempFile(suffix=".nc") as tmp1,
        GMTTempFile(suffix=".nc") as tmp2,
        GMTTempFile(suffix=".nc") as tmpout,
    ):
        grdcut(grid, region=[-53, -49, -19, -16], outgrid=tmp1.name)
        grdcut(grid, region=[-53, -49, -22, -19], outgrid=tmp2.name)
        result = grdpaste(grid1=tmp1.name, grid2=tmp2.name, outgrid=tmpout.name)
        assert result is None  # grdpaste returns None if output to a file
        temp_grid = xr.load_dataarray(tmpout.name, engine="gmt", raster_kind="grid")
        assert isinstance(temp_grid, xr.DataArray)
        assert temp_grid.shape == (6, 4)
        # Check that the result has the expected min and max values
        assert temp_grid.min().values == 345.5
        assert temp_grid.max().values == max(
            grid_top.max().values, grid_bottom.max().values
        )


# TODO(GMT>=6.7): Remove the xfail marker for GMT<6.7.
@pytest.mark.xfail(
    condition=Version(__gmt_version__) < Version("6.7"),
    reason="Upstream bug fixed in https://github.com/GenericMappingTools/gmt/pull/8901",
)
def test_grdpaste_file_in_xarray_out(grid):
    """
    Test grdpaste with file input and xarray output.
    """
    with (
        GMTTempFile(suffix=".nc") as tmp1,
        GMTTempFile(suffix=".nc") as tmp2,
    ):
        grdcut(grid, region=[-53, -49, -19, -16], outgrid=tmp1.name)
        grdcut(grid, region=[-53, -49, -22, -19], outgrid=tmp2.name)
        result = grdpaste(grid1=tmp1.name, grid2=tmp2.name)
        assert isinstance(result, xr.DataArray)
        assert result.shape == (6, 4)


# TODO(GMT>=6.7): Remove the xfail marker for GMT<6.7.
@pytest.mark.xfail(
    condition=Version(__gmt_version__) < Version("6.7"),
    reason="Requires GMT dev version (https://github.com/GenericMappingTools/gmt/pull/8901)",
)
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
    # Check that the result has the expected min and max values
    assert result.min().values == min(grid_top.min().values, grid_bottom.min().values)
    assert result.max().values == max(grid_top.max().values, grid_bottom.max().values)


# TODO(GMT>=6.7): Remove the xfail marker for GMT<6.7.
@pytest.mark.xfail(
    condition=Version(__gmt_version__) < Version("6.7"),
    reason="Requires GMT dev version (https://github.com/GenericMappingTools/gmt/pull/8901)",
)
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
