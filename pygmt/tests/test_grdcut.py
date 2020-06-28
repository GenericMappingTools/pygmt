"""
Tests for grdcut
"""
import os
import numpy as np
import pytest
import xarray as xr

from .. import grdcut, grdinfo
from ..datasets import load_earth_relief
from ..exceptions import GMTInvalidInput
from ..helpers import GMTTempFile


def test_grdcut_file_in_file_out():
    "grduct an input grid file, and output to a grid file"
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdcut("@earth_relief_01d", outgrid=tmpfile.name, region="0/180/0/90")
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        result = grdinfo(tmpfile.name, C=True)
        assert result == "0 180 0 90 -8592.5 5559 1 1 181 91\n"


def test_grdcut_file_in_dataarray_out():
    "grdcut an input grid file, and output as DataArray"
    outgrid = grdcut("@earth_relief_01d", region="0/180/0/90")
    assert isinstance(outgrid, xr.DataArray)
    # check information of the output grid
    # the '@earth_relief_01d' is in pixel registration, so the grid range is
    # not exactly 0/180/0/90
    assert outgrid.coords["lat"].data.min() == 0.0
    assert outgrid.coords["lat"].data.max() == 90.0
    assert outgrid.coords["lon"].data.min() == 0.0
    assert outgrid.coords["lon"].data.max() == 180.0
    assert outgrid.data.min() == -8592.5
    assert outgrid.data.max() == 5559
    assert outgrid.sizes["lat"] == 91
    assert outgrid.sizes["lon"] == 181


def test_grdcut_dataarray_in_file_out():
    "grdcut an input DataArray, and output to a grid file"
    # Not supported yet.
    # See https://github.com/GenericMappingTools/gmt/pull/3532


def test_grdcut_dataarray_in_dataarray_out():
    "grdcut an input DataArray, and output to a grid file"
    # Not supported yet.
    # See https://github.com/GenericMappingTools/gmt/pull/3532


def test_grdcut_dataarray_in_fail():
    "Make sure that grdcut fails correctly if DataArray is the input grid"
    with pytest.raises(NotImplementedError):
        grid = load_earth_relief()
        grdcut(grid, region="0/180/0/90")


def test_grdcut_fails():
    "Check that grdcut fails correctly"
    with pytest.raises(GMTInvalidInput):
        grdcut(np.arange(10).reshape((5, 2)))
