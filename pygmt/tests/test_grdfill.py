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
    grid = load_earth_relief(registration="pixel", region=[-5, 5, -5, 5])
    grid[3:5, 3:5] = np.nan
    grid[5:7, 5:7] = np.inf
    return grid


@pytest.fixture(scope="module", name="expected_grid")
def fixture_grid_result():
    """
    Load the expected grdcut grid result.
    """
    return xr.DataArray(
        data=[
            [
                -4560.0,
                -4421.0,
                -4341.0,
                -4664.0,
                -4578.0,
                -4642.0,
                -4796.0,
                -5001.5,
                -4578.0,
                -4678.0,
            ],
            [
                -4684.5,
                -4759.5,
                -4615.0,
                -4389.5,
                -4034.0,
                -4130.0,
                -3763.5,
                -4578.0,
                -4262.5,
                -4667.0,
            ],
            [
                -4875.0,
                -4867.0,
                -4762.0,
                -4788.0,
                -4680.5,
                -4545.0,
                -4377.0,
                -4095.5,
                -3960.0,
                -4166.0,
            ],
            [
                -4988.0,
                -5068.0,
                -4964.5,
                20.0,
                20.0,
                -4396.5,
                -4469.5,
                -4305.5,
                -4111.5,
                -3679.0,
            ],
            [
                -5115.5,
                -5130.5,
                -5019.5,
                20.0,
                20.0,
                -4747.5,
                -4431.5,
                -4176.0,
                -4169.5,
                -3992.0,
            ],
            [
                -5095.5,
                -5124.0,
                -5102.5,
                -5040.0,
                -4967.0,
                np.inf,
                np.inf,
                -4422.0,
                -4213.0,
                -3966.5,
            ],
            [
                -5074.0,
                -5099.5,
                -5122.0,
                -5059.5,
                -4984.5,
                np.inf,
                np.inf,
                -4452.0,
                -4208.0,
                -3865.5,
            ],
            [
                -4760.5,
                -4895.0,
                -5069.5,
                -5105.0,
                -4937.0,
                -4708.0,
                -4537.5,
                -4370.5,
                -4062.5,
                -3742.5,
            ],
            [
                -4154.0,
                -4148.5,
                -4115.5,
                -4996.0,
                -4762.0,
                -4599.0,
                -4355.5,
                -4120.5,
                -3771.0,
                -3064.5,
            ],
            [
                -2899.5,
                -2042.0,
                -656.0,
                -160.0,
                -3484.5,
                -3897.5,
                -3833.0,
                -3833.0,
                -2966.5,
                -1247.5,
            ],
        ],
        coords=dict(
            lon=[-4.5, -3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5, 4.5],
            lat=[-4.5, -3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5, 4.5],
        ),
        dims=["lat", "lon"],
    )


def test_grdfill_dataarray_out(grid, expected_grid):
    """
    grdfill with a DataArray output.
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
    grdfill with an outgrid set.
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
