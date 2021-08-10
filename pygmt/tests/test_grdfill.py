"""
Tests for grdfill.
"""
import os

import numpy as np
import pytest
import xarray as xr
from pygmt import grdfill, grdinfo
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file and set value(s) to
    NaN.
    """
    grid = load_earth_relief(registration="pixel", region=[-5, 5, -5, 5])
    grid[3:5, 3:5] = np.nan
    grid[5:7, 5:7] = np.inf
    return grid


def test_grdfill_dataarray_out(grid):
    """
    grdfill with a DataArray output.
    """
    result = grdfill(grid=grid, mode="c20")
    # check information of the output grid
    assert isinstance(result, xr.DataArray)
    assert result[4, 4] == 20
    assert result[5, 5] == np.inf
    assert not result.isnull().all()  # check that no NaN values exists
    assert result.gmt.gtype == 1  # Geographic grid
    assert result.gmt.registration == 1  # Pixel registration


def test_grdfill_file_out(grid):
    """
    grdfill with an outgrid set.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdfill(grid=grid, mode="c20", outgrid=tmpfile.name)
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        result = grdinfo(tmpfile.name, per_column=True).strip()
        assert result == "-5 5 -5 5 -5130.5 inf 1 1 10 10 1 1"


def test_grdfill_required_args(grid):
    """
    Test that grdfill fails without arguments for `mode` and `L`.
    """
    with pytest.raises(GMTInvalidInput):
        grdfill(grid=grid)
