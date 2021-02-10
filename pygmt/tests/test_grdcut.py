"""
Tests for grdcut.
"""
import os

import numpy as np
import pytest
import xarray as xr
from pygmt import grdcut, grdinfo
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(registration="pixel")


def test_grdcut_file_in_file_out():
    """
    grdcut an input grid file, and output to a grid file.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdcut("@earth_relief_01d", outgrid=tmpfile.name, region="0/180/0/90")
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        result = grdinfo(tmpfile.name, per_column=True)
        assert result == "0 180 0 90 -8182 5651.5 1 1 180 90 1 1\n"


def test_grdcut_file_in_dataarray_out():
    """
    grdcut an input grid file, and output as DataArray.
    """
    outgrid = grdcut("@earth_relief_01d", region="0/180/0/90")
    assert isinstance(outgrid, xr.DataArray)
    assert outgrid.gmt.registration == 1  # Pixel registration
    assert outgrid.gmt.gtype == 1  # Geographic type
    # check information of the output grid
    # the '@earth_relief_01d' is in pixel registration, so the grid range is
    # not exactly 0/180/0/90
    assert outgrid.coords["lat"].data.min() == 0.5
    assert outgrid.coords["lat"].data.max() == 89.5
    assert outgrid.coords["lon"].data.min() == 0.5
    assert outgrid.coords["lon"].data.max() == 179.5
    assert outgrid.data.min() == -8182.0
    assert outgrid.data.max() == 5651.5
    assert outgrid.sizes["lat"] == 90
    assert outgrid.sizes["lon"] == 180


def test_grdcut_dataarray_in_file_out(grid):
    """
    grdcut an input DataArray, and output to a grid file.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdcut(grid, outgrid=tmpfile.name, region="0/180/0/90")
        assert result is None  # grdcut returns None if output to a file
        result = grdinfo(tmpfile.name, per_column=True)
        assert result == "0 180 0 90 -8182 5651.5 1 1 180 90 1 1\n"


def test_grdcut_dataarray_in_dataarray_out(grid):
    """
    grdcut an input DataArray, and output as DataArray.
    """
    outgrid = grdcut(grid, region="0/180/0/90")
    assert isinstance(outgrid, xr.DataArray)
    # check information of the output grid
    # the '@earth_relief_01d' is in pixel registration, so the grid range is
    # not exactly 0/180/0/90
    assert outgrid.coords["lat"].data.min() == 0.5
    assert outgrid.coords["lat"].data.max() == 89.5
    assert outgrid.coords["lon"].data.min() == 0.5
    assert outgrid.coords["lon"].data.max() == 179.5
    assert outgrid.data.min() == -8182.0
    assert outgrid.data.max() == 5651.5
    assert outgrid.sizes["lat"] == 90
    assert outgrid.sizes["lon"] == 180


def test_grdcut_fails():
    """
    Check that grdcut fails correctly.
    """
    with pytest.raises(GMTInvalidInput):
        grdcut(np.arange(10).reshape((5, 2)))
