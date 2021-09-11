"""
Tests for dimfilter.
"""
import os

import numpy.testing as npt
import pytest
from pygmt import dimfilter
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(resolution="30m", region=[-5, 5, -5, 5])


def test_dimfilter_outgrid(grid):
    """
    Test the required parameters for dimfilter with a set outgrid.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = dimfilter(grid=grid, outgrid=tmpfile.name, filter="m600", distance=4, sectors="l6")
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists


def test_grdgradient_no_outgrid(grid):
    """
    Test the required parameters for dimfilter with no set outgrid.
    """
    temp_grid = dimfilter(grid=grid, filter="m600", distance=4, sectors="l6")
    assert temp_grid.dims == ("lat", "lon")
    assert temp_grid.gmt.gtype == 1  # Geographic grid
    assert temp_grid.gmt.registration == 1  # Pixel registration
    npt.assert_allclose(temp_grid.min(), -5125)
    npt.assert_allclose(temp_grid.max(), -3750.5)
    npt.assert_allclose(temp_grid.median(), -4826.5)
    npt.assert_allclose(temp_grid.mean(), -4789.791)

def test_dimfilter_fails(grid):
    """
    Check that dimfilter fails correctly when sector, 
    filters, and distance are not specified..
    """
    with pytest.raises(GMTInvalidInput):
        dimfilter(grid=grid)