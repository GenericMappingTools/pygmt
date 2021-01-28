"""
Tests for grdfilter.
"""
import numpy as np
import pytest
import xarray as xr
from pygmt import grdfilter, grdinfo
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(registration="pixel")


def test_grfilter_dataarray_in_dataarray_out(grid):
    """
    grdfilter an input DataArray, and output as DataArray.
    """
    # grid = load_earth_relief(registration="pixel")
    result = grdfilter(grid=grid, filter="g600", distance="4")
    # check information of the output grid
    assert isinstance(result, xr.DataArray)
    assert result.coords["lat"].data.min() == -89.5
    assert result.coords["lat"].data.max() == 89.5
    assert result.coords["lon"].data.min() == -179.5
    assert result.coords["lon"].data.max() == 179.5
    assert result.sizes["lat"] == 180
    assert result.sizes["lon"] == 360


def test_grdfilter_dataarray_in_file_out(grid):
    """
    grdfilter an input DataArray, and output to a grid file.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdfilter(grid, outgrid=tmpfile.name, filter="g600", distance="4")
        assert result is None  # grdcut returns None if output to a file
        result = grdinfo(tmpfile.name, C=True)
        assert (
            result == "-180 180 -90 90 -6147.47265625 5164.11572266 1 1 360 180 1 1\n"
        )


def test_grdfilter_fails():
    """
    Check that grdfilter fails correctly.
    """
    with pytest.raises(GMTInvalidInput):
        grdfilter(np.arange(10).reshape((5, 2)))
