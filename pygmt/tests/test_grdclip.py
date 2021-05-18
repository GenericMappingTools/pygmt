"""
Tests for grdclip.
"""
import os

import numpy.testing as npt
import pytest
from pygmt import grdclip, grdinfo
from pygmt.datasets import load_earth_relief
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(resolution="01d", region=[-5, 5, -5, 5])


def test_grdclip_outgrid(grid):
    """
    Test the below and above parameters for grdclip and creates a test outgrid.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdclip(
            grid=grid, outgrid=tmpfile.name, below=[-1500, -1800], above=[-200, 40]
        )
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        result = (
            grdinfo(grid=tmpfile.name, force_scan=0, per_column="n").strip().split()
        )
    assert int(result[4]) == -1800  # minimum value
    assert int(result[5]) == 40  # maximum value


def test_grdclip_no_outgrid(grid):
    """
    Test the below and above parameters for grdclip with no set outgrid.
    """
    temp_grid = grdclip(grid=grid, below=[-1500, -1800], above=[-200, 40])
    assert temp_grid.dims == ("lat", "lon")
    assert temp_grid.gmt.gtype == 1  # Geographic grid
    assert temp_grid.gmt.registration == 1  # Pixel registration
    npt.assert_allclose(temp_grid.min(), -1800)
    npt.assert_allclose(temp_grid.max(), 40)
