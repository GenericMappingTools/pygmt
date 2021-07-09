"""
Tests for grdproject.
"""
import os

import pytest
from pygmt import grdinfo, grdproject
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(resolution="01d", region=[-5, 5, -5, 5])


def test_grdproject_file_out(grid):
    """
    grdproject with an outgrid set.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdproject(grid=grid, projection="M10c", outgrid=tmpfile.name)
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        result = grdinfo(tmpfile.name, per_column=True).strip().split()


def test_grdproject_no_outgrid(grid):
    """
    Test grdproject with no set outgrid.
    """
    assert grid.gmt.gtype == 1  # Geographic grid
    temp_grid = grdproject(grid=grid, projection="M10c")
    assert temp_grid.dims == ("y", "x")
    assert temp_grid.gmt.gtype == 0  # Rectangular grid
    assert temp_grid.gmt.registration == 1  # Pixel registration


def test_grdproject_fails(grid):
    """
    Check that grdproject fails correctly.
    """
    with pytest.raises(GMTInvalidInput):
        grdproject(grid=grid)
