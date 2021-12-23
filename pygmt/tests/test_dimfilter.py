"""
Tests for dimfilter.
"""
import os

import numpy.testing as npt
import pytest
import xarray as xr
from pygmt import dimfilter, load_dataarray
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput
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
    Load the expected dimfilter grid result.
    """
    return xr.DataArray(
        data=[
            [397.0, 393.0, 377.5, 382.75, 419.0, 435.5],
            [361.75, 359.0, 364.5, 415.5, 411.0, 373.5],
            [321.5, 361.75, 373.5, 379.5, 369.0, 379.5],
            [292.5, 324.0, 356.0, 361.5, 337.0, 361.5],
            [306.0, 282.5, 310.25, 324.0, 353.0, 372.5],
        ],
        coords=dict(
            lon=[124.5, 125.5, 126.5, 127.5, 128.5, 129.5],
            lat=[-24.5, -23.5, -22.5, -21.5, -20.5],
        ),
        dims=["lat", "lon"],
    )


def test_dimfilter_outgrid(grid, expected_grid):
    """
    Test the required parameters for dimfilter with a set outgrid.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = dimfilter(
            grid=grid, outgrid=tmpfile.name, filter="m600", distance=4, sectors="l6"
        )
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdgradient_no_outgrid(grid, expected_grid):
    """
    Test the required parameters for dimfilter with no set outgrid.
    """
    result = dimfilter(grid=grid, filter="m600", distance=4, sectors="l6")
    assert result.dims == ("lat", "lon")
    assert result.gmt.gtype == 1  # Geographic grid
    assert result.gmt.registration == 1  # Pixel registration
    xr.testing.assert_allclose(a=result, b=expected_grid)


def test_dimfilter_fails(grid):
    """
    Check that dimfilter fails correctly when sector, filters, and distance are
    not specified.
    """
    with pytest.raises(GMTInvalidInput):
        dimfilter(grid=grid)
