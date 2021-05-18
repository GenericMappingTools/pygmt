"""
Tests for grdclip.
"""
import os

import numpy as np
import pytest
import xarray as xr
from pygmt import grdfill, grdinfo
from pygmt.datasets import load_earth_relief
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file and set value(s) to
    NaN.
    """
    grid = load_earth_relief(registration="pixel")
    grid[10, 10] = np.nan
    return grid


def test_grdfill_dataarray_out(grid):
    """
    grdfill with a DataArray output.
    """
    result = grdfill(grid=grid, mode="c20")
    # check information of the output grid
    assert isinstance(result, xr.DataArray)
    assert result[10, 10] == 20


def test_grdfill_file_out(grid):
    """
    grdfill with an outgrid set.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdfill(grid=grid, mode="c20", outgrid=tmpfile.name)
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        result = grdinfo(tmpfile.name, per_column=True).strip()
        assert result == "-180 180 -90 90 -8182 5651.5 1 1 360 180 1 1"
