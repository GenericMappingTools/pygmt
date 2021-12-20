"""
Tests for grdsample.
"""
import os

import pytest
import xarray as xr
from pygmt import grdsample, load_dataarray
from pygmt.datasets import load_earth_relief
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(
        resolution="01d", registration="pixel", region=[124, 130, -25, -20]
    )


@pytest.fixture(scope="module", name="expected_grid")
def fixture_grid_result():
    """
    Load the expected grdsample grid result.
    """
    return xr.DataArray(
        data=[
            [433.65625, 447.96875, 540.0625],
            [397.28125, 386.15625, 484.125],
            [334.96875, 417.25, 385.1875],
            [303.40625, 373.625, 395.0],
            [311.15625, 321.15625, 389.875],
        ],
        coords=dict(
            lon=[
                125.0,
                127.0,
                129.0,
            ],
            lat=[
                -24.5,
                -23.5,
                -22.5,
                -21.5,
                -20.5,
            ],
        ),
        dims=["lat", "lon"],
    )


def test_grdsample_file_out(grid, expected_grid):
    """
    Test grdsample with an outgrid set and the spacing is changed.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdsample(grid=grid, outgrid=tmpfile.name, spacing=[2, 1])
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdsample_dataarray_out(grid, expected_grid):
    """
    Test grdsample with no outgrid set and the spacing is changed.
    """
    result = grdsample(grid=grid, spacing=[2, 1])
    # check information of the output grid
    assert isinstance(result, xr.DataArray)
    assert result.gmt.gtype == 1  # Geographic grid
    assert result.gmt.registration == 1  # Pixel registration
    # check information of the output grid
    xr.testing.assert_allclose(a=result, b=expected_grid)


def test_grdsample_registration_changes(grid):
    """
    Test grdsample with no set outgrid and applying registration changes.
    """
    assert grid.gmt.registration == 1  # Pixel registration
    translated_grid = grdsample(grid=grid, translate=True)
    assert translated_grid.gmt.registration == 0  # Gridline registration
    registration_grid = grdsample(grid=translated_grid, registration="p")
    assert registration_grid.gmt.registration == 1  # Pixel registration
