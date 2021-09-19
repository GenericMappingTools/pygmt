"""
Tests for grdhisteq.
"""
import os

import pytest
import xarray.testing as xrt
from pygmt import grdhisteq
from pygmt.datasets import load_earth_relief
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(resolution="01d", region=[-5, 5, -5, 5])


def test_grdhisteq_outgrid(grid):
    """
    Test the gaussian parameter of grdhisteq with a set outgrid.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdhisteq(grid=grid, gaussian=True, outgrid=tmpfile.name)
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists


def test_grdhisteq_no_outgrid(grid):
    """
    Test the quadratic and region parameters for grdhisteq with no set outgrid.
    """
    temp_grid = grdhisteq(grid=grid, quadratic=True, region=[-3, 1, 2, 5])
    assert temp_grid.gmt.gtype == 1  # Geographic grid
    assert temp_grid.gmt.registration == 1  # Pixel registration
    expected_grid = xr.DataArray(
        data=[[4.0, 0.0, 8.0, 11.0], [13.0, 4.0, 8.0, 13.0], [15.0, 15.0, 15.0, 15.0]],
        coords=dict(lon=[-2.5, -1.5, -0.5, 0.5], lat=[2.5, 3.5, 4.5]),
        dims=["lat", "lon"],
    )
    xrt.assert_allclose(a=temp_grid, b=expected_grid)
