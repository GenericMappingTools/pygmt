"""
Test the behaviour of the GMTDataArrayAccessor class.
"""
import os
import sys
from pathlib import Path

import pytest
import xarray as xr
from packaging.version import Version
from pygmt import __gmt_version__, which
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput


def test_accessor_gridline_cartesian():
    """
    Check that a grid returns a registration value of 0 when Gridline
    registered, and a gtype value of 1 when using Geographic coordinates.
    """
    fname = which(fname="@test.dat.nc", download="a")
    grid = xr.open_dataarray(fname)
    assert grid.gmt.registration == 0  # gridline registration
    assert grid.gmt.gtype == 0  # cartesian coordinate type


def test_accessor_pixel_geographic():
    """
    Check that a grid returns a registration value of 1 when Pixel registered,
    and a gtype value of 0 when using Cartesian coordinates.
    """
    fname = which(fname="@earth_relief_01d_p", download="a")
    grid = xr.open_dataarray(fname, engine="netcdf4")
    assert grid.gmt.registration == 1  # pixel registration
    assert grid.gmt.gtype == 1  # geographic coordinate type


def test_accessor_set_pixel_registration():
    """
    Check that we can set a grid to be Pixel registered with a registration
    value of 1.
    """
    grid = xr.DataArray(data=[[0.1, 0.2], [0.3, 0.4]])
    assert grid.gmt.registration == 0  # default to gridline registration
    grid.gmt.registration = 1  # set to pixel registration
    assert grid.gmt.registration == 1  # ensure changed to pixel registration


def test_accessor_set_geographic_cartesian_roundtrip():
    """
    Check that we can set a grid to switch between the default Cartesian
    coordinate type using a gtype of 1, set it to Geographic 0, and then back
    to Cartesian again 1.
    """
    grid = xr.DataArray(data=[[0.1, 0.2], [0.3, 0.4]])
    assert grid.gmt.gtype == 0  # default to cartesian coordinate type
    grid.gmt.gtype = 1  # set to geographic type
    assert grid.gmt.gtype == 1  # ensure changed to geographic coordinate type
    grid.gmt.gtype = 0  # set back to cartesian type
    assert grid.gmt.gtype == 0  # ensure changed to cartesian coordinate type


def test_accessor_set_non_boolean():
    """
    Check that setting non boolean values on registration and gtype do not
    work.
    """
    grid = xr.DataArray(data=[[0.1, 0.2], [0.3, 0.4]])

    with pytest.raises(GMTInvalidInput):
        grid.gmt.registration = "2"

    with pytest.raises(GMTInvalidInput):
        grid.gmt.gtype = 2


@pytest.mark.skipif(
    Version(__gmt_version__) < Version("6.4.0"),
    reason="Upstream bug fixed in https://github.com/GenericMappingTools/gmt/pull/6615",
)
@pytest.mark.xfail(
    condition=sys.platform == "win32" and Version(__gmt_version__) < Version("6.5.0"),
    reason="Upstream bug fixed in https://github.com/GenericMappingTools/gmt/pull/7573",
)
def test_accessor_sliced_datacube():
    """
    Check that a 2-D grid which is sliced from an n-dimensional datacube works
    with accessor methods.

    This is a regression test for
    https://github.com/GenericMappingTools/pygmt/issues/1578.
    """
    try:
        fname = which(
            "https://github.com/pydata/xarray-data/raw/master/eraint_uvz.nc",
            download="u",
        )
        with xr.open_dataset(fname) as dataset:
            grid = dataset.sel(level=500, month=1, drop=True).z

        assert grid.gmt.registration == 0  # gridline registration
        assert grid.gmt.gtype == 1  # geographic coordinate type
    finally:
        os.remove(fname)


def test_accessor_grid_source_file_not_exist():
    """
    Check that the accessor fallbacks to the default registration and gtype
    when the grid source file (i.e., grid.encoding["source"]) doesn't exist.
    """
    # Load the 05m earth relief grid, which is stored as tiles
    grid = load_earth_relief(
        resolution="05m", region=[0, 5, -5, 5], registration="pixel"
    )
    # Registration and gtype are correct
    assert grid.gmt.registration == 1
    assert grid.gmt.gtype == 1
    # The source grid file is defined but doesn't exist
    assert grid.encoding["source"].endswith(".nc")
    assert not Path(grid.encoding["source"]).exists()

    # For a sliced grid, fallback to default registration and gtype,
    # because the source grid file doesn't exist.
    sliced_grid = grid[1:3, 1:3]
    assert sliced_grid.gmt.registration == 0
    assert sliced_grid.gmt.gtype == 0

    # Still possible to manually set registration and gtype
    sliced_grid.gmt.registration = 1
    sliced_grid.gmt.gtype = 1
    assert sliced_grid.gmt.registration == 1
    assert sliced_grid.gmt.gtype == 1
