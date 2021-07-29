"""
Tests for grdhisteq.
"""
import os

import numpy.testing as npt
import pytest
from pygmt import grdhisteq, grdinfo
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
    Test the azimuth and direction parameters for grdhisteq with a set outgrid.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdhisteq(grid=grid, outgrid=tmpfile.name)
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        result = (
            grdinfo(grid=tmpfile.name, force_scan="a", per_column="n").strip().split()
        )


def test_grdhisteq_no_outgrid(grid):
    """
    Test the azimuth and direction parameters for grdhisteq with no set
    outgrid.
    """
    temp_grid = grdhisteq(grid=grid)
    assert temp_grid.dims == ("lat", "lon")
    assert temp_grid.gmt.gtype == 1  # Geographic grid
    assert temp_grid.gmt.registration == 1  # Pixel registration
