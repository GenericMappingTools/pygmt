"""
Tests for grdfilter.
"""
import os

import numpy as np
import numpy.testing as npt
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


def test_grdfilter_dataarray_in_dataarray_out(grid):
    """
    grdfilter an input DataArray, and output as DataArray.
    """
    result = grdfilter(grid=grid, filter="g600", distance="4")
    # check information of the output grid
    assert isinstance(result, xr.DataArray)
    assert result.coords["lat"].data.min() == -89.5
    assert result.coords["lat"].data.max() == 89.5
    assert result.coords["lon"].data.min() == -179.5
    assert result.coords["lon"].data.max() == 179.5
    npt.assert_almost_equal(result.data.min(), -6147.4907, decimal=2)
    npt.assert_almost_equal(result.data.max(), 5164.06, decimal=2)
    assert result.sizes["lat"] == 180
    assert result.sizes["lon"] == 360


def test_grdfilter_dataarray_in_file_out(grid):
    """
    grdfilter an input DataArray, and output to a grid file.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdfilter(grid, outgrid=tmpfile.name, filter="g600", distance="4")
        assert result is None  # grdfilter returns None if output to a file
        result = grdinfo(tmpfile.name, per_column=True)
        assert (
            result == "-180 180 -90 90 -6147.49072266 5164.06005859 1 1 360 180 1 1\n"
        )


def test_grdfilter_file_in_dataarray_out():
    """
    grdfilter an input grid file, and output as DataArray.
    """
    outgrid = grdfilter(
        "@earth_relief_01d", region="0/180/0/90", filter="g600", distance="4"
    )
    assert isinstance(outgrid, xr.DataArray)
    assert outgrid.gmt.registration == 1  # Pixel registration
    assert outgrid.gmt.gtype == 1  # Geographic type
    # check information of the output DataArray
    # the '@earth_relief_01d' is in pixel registration, so the grid range is
    # not exactly 0/180/0/90
    assert outgrid.coords["lat"].data.min() == 0.5
    assert outgrid.coords["lat"].data.max() == 89.5
    assert outgrid.coords["lon"].data.min() == 0.5
    assert outgrid.coords["lon"].data.max() == 179.5
    npt.assert_almost_equal(outgrid.data.min(), -6147.4907, decimal=2)
    npt.assert_almost_equal(outgrid.data.max(), 5164.06, decimal=2)
    assert outgrid.sizes["lat"] == 90
    assert outgrid.sizes["lon"] == 180


def test_grdfilter_file_in_file_out():
    """
    grdfilter an input grid file, and output to a grid file.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdfilter(
            "@earth_relief_01d",
            outgrid=tmpfile.name,
            region=[0, 180, 0, 90],
            filter="g600",
            distance="4",
        )
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        result = grdinfo(tmpfile.name, per_column=True)
        assert result == "0 180 0 90 -6147.49072266 5164.06005859 1 1 180 90 1 1\n"


def test_grdfilter_fails():
    """
    Check that grdfilter fails correctly.
    """
    with pytest.raises(GMTInvalidInput):
        grdfilter(np.arange(10).reshape((5, 2)))
