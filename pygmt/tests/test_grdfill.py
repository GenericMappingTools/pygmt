"""
Tests for grdfill.
"""
import os

import numpy as np
import pytest
import xarray as xr
from pygmt import grdfill, load_dataarray
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file and set value(s) to
    NaN.
    """
    grid = load_earth_relief(registration="pixel", region=[125, 130, -25, -20])
    grid[2:4, 1:3] = np.nan
    grid[0:2, 2:4] = np.inf
    return grid


@pytest.fixture(scope="module", name="expected_grid")
def fixture_grid_result():
    """
    Load the expected grdfill grid result.
    """
    return xr.DataArray(
        data=[
            [442.5, 439.0, np.inf, np.inf, 508.0],
            [393.0, 364.5, np.inf, np.inf, 506.5],
            [362.0, 20.0, 20.0, 373.5, 402.5],
            [321.5, 20.0, 20.0, 356.0, 422.5],
            [282.5, 318.0, 326.5, 379.5, 383.5],
        ],
        coords=dict(
            lon=[125.5, 126.5, 127.5, 128.5, 129.5],
            lat=[-24.5, -23.5, -22.5, -21.5, -20.5],
        ),
        dims=["lat", "lon"],
    )


def test_grdfill_dataarray_out(grid, expected_grid):
    """
    Test grdfill with a DataArray output.
    """
    result = grdfill(grid=grid, mode="c20")
    # check information of the output grid
    assert isinstance(result, xr.DataArray)
    assert result.gmt.gtype == 1  # Geographic grid
    assert result.gmt.registration == 1  # Pixel registration
    # check information of the output grid
    xr.testing.assert_allclose(a=result, b=expected_grid)


def test_grdfill_file_out(grid, expected_grid):
    """
    Test grdfill with an outgrid set.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdfill(grid=grid, mode="c20", outgrid=tmpfile.name)
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdfill_required_args(grid):
    """
    Test that grdfill fails without arguments for `mode` and `L`.
    """
    with pytest.raises(GMTInvalidInput):
        grdfill(grid=grid)
