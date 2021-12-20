"""
Tests for grdfilter.
"""
import os

import numpy as np
import numpy.testing as npt
import pytest
import xarray as xr
from pygmt import grdfilter, load_dataarray
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(registration="pixel", region=[125, 130, -25, -20])


@pytest.fixture(scope="module", name="expected_grid")
def fixture_grid_result():
    """
    Load the expected grdfill grid result.
    """
    return xr.DataArray(
        data=[
            [420.08807, 426.77594, 447.09592, 472.27304, 489.7439],
            [396.38043, 404.6039, 422.78824, 443.64108, 460.98114],
            [371.33716, 383.5158, 395.80002, 406.05035, 418.44943],
            [342.4835, 357.37195, 368.98615, 380.39688, 394.0022],
            [316.79086, 332.9292, 350.14505, 369.29675, 384.69217],
        ],
        coords=dict(
            lon=[125.5, 126.5, 127.5, 128.5, 129.5],
            lat=[-24.5, -23.5, -22.5, -21.5, -20.5],
        ),
        dims=["lat", "lon"],
    )


def test_grdfilter_dataarray_in_dataarray_out(grid, expected_grid):
    """
    grdfilter an input DataArray, and output as DataArray.
    """
    result = grdfilter(grid=grid, filter="g600", distance="4")
    # check information of the output grid
    assert isinstance(result, xr.DataArray)
    assert result.gmt.gtype == 1  # Geographic grid
    assert result.gmt.registration == 1  # Pixel registration
    # check information of the output grid
    xr.testing.assert_allclose(a=result, b=expected_grid)


def test_grdfilter_dataarray_in_file_out(grid, expected_grid):
    """
    grdfilter an input DataArray, and output to a grid file.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdfilter(grid, outgrid=tmpfile.name, filter="g600", distance="4")
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_grdfilter_fails():
    """
    Check that grdfilter fails correctly.
    """
    with pytest.raises(GMTInvalidInput):
        grdfilter(np.arange(10).reshape((5, 2)))
