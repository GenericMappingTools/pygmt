"""
Test the behaviour of the GMTDataArrayAccessor class.
"""

import importlib
import sys
from pathlib import Path

import pytest
import xarray as xr
from packaging.version import Version
from pygmt import which
from pygmt.clib import __gmt_version__
from pygmt.datasets import load_earth_relief
from pygmt.enums import GridRegistration, GridType
from pygmt.exceptions import GMTValueError

_HAS_NETCDF4 = bool(importlib.util.find_spec("netCDF4"))


def test_xarray_accessor_gridline_cartesian():
    """
    Check that the accessor returns the correct registration and gtype values for a
    Cartesian, gridline-registered grid.
    """
    grid = xr.load_dataarray("@test.dat.nc", engine="gmt", raster_kind="grid")
    assert grid.gmt.registration is GridRegistration.GRIDLINE
    assert grid.gmt.gtype is GridType.CARTESIAN


def test_xarray_accessor_pixel_geographic():
    """
    Check that the accessor returns the correct registration and gtype values for a
    geographic, pixel-registered grid.
    """
    grid = xr.load_dataarray("@earth_relief_01d_p", engine="gmt", raster_kind="grid")
    assert grid.gmt.registration is GridRegistration.PIXEL
    assert grid.gmt.gtype is GridType.GEOGRAPHIC


def test_xarray_accessor_set_registration():
    """
    Check that we can set the registration of a grid.
    """
    grid = xr.DataArray(data=[[0.1, 0.2], [0.3, 0.4]])
    # Default to gridline registration
    assert grid.gmt.registration is GridRegistration.GRIDLINE == 0

    # Set the registration to pixel
    grid.gmt.registration = GridRegistration.PIXEL
    assert grid.gmt.registration is GridRegistration.PIXEL == 1

    # Set the registration to gridline
    grid.gmt.registration = GridRegistration.GRIDLINE
    assert grid.gmt.registration is GridRegistration.GRIDLINE == 0

    # Set the registration to pixel but using a numerical value
    grid.gmt.registration = 1
    assert grid.gmt.registration is GridRegistration.PIXEL == 1

    # Set the registration to gridline but using a numerical value
    grid.gmt.registration = 0
    assert grid.gmt.registration is GridRegistration.GRIDLINE == 0


@pytest.mark.benchmark
def test_xarray_accessor_set_gtype():
    """
    Check that we can set the gtype of a grid.
    """
    grid = xr.DataArray(data=[[0.1, 0.2], [0.3, 0.4]])
    assert grid.gmt.gtype is GridType.CARTESIAN == 0  # Default gtype

    # Set the gtype to geographic
    grid.gmt.gtype = GridType.GEOGRAPHIC
    assert grid.gmt.gtype is GridType.GEOGRAPHIC == 1

    # Set the gtype to Cartesian
    grid.gmt.gtype = GridType.CARTESIAN
    assert grid.gmt.gtype is GridType.CARTESIAN == 0

    # Set the gtype to geographic but using a numerical value
    grid.gmt.gtype = 1
    assert grid.gmt.gtype is GridType.GEOGRAPHIC == 1

    # Set the gtype to Cartesian but using a numerical value
    grid.gmt.gtype = 0
    assert grid.gmt.gtype is GridType.CARTESIAN == 0


def test_xarray_accessor_set_invalid_registration_and_gtype():
    """
    Check that setting invalid values on registration and gtype do not work.
    """
    grid = xr.DataArray(data=[[0.1, 0.2], [0.3, 0.4]])

    with pytest.raises(GMTValueError):
        grid.gmt.registration = "2"
    with pytest.raises(GMTValueError):
        grid.gmt.registration = "pixel"
    with pytest.raises(GMTValueError):
        grid.gmt.gtype = 2
    with pytest.raises(GMTValueError):
        grid.gmt.gtype = "geographic"


# TODO(GMT>=6.5.0): Remove the xfail marker for GMT>=6.5.0.
@pytest.mark.skipif(condition=not _HAS_NETCDF4, reason="netCDF4 is not installed")
@pytest.mark.xfail(
    condition=sys.platform == "win32" and Version(__gmt_version__) < Version("6.5.0"),
    reason="Upstream bug fixed in https://github.com/GenericMappingTools/gmt/pull/7573",
)
def test_xarray_accessor_sliced_datacube():
    """
    Check that a 2-D grid which is sliced from an n-dimensional datacube works with
    accessor methods.

    This is a regression test for
    https://github.com/GenericMappingTools/pygmt/issues/1578.
    """
    try:
        fname = which(
            "https://github.com/pydata/xarray-data/raw/master/eraint_uvz.nc",
            download="u",
        )
        with xr.open_dataset(fname, engine="netcdf4") as dataset:
            grid = dataset.sel(level=500, month=1, drop=True).z

        assert grid.gmt.registration is GridRegistration.GRIDLINE
        assert grid.gmt.gtype is GridType.GEOGRAPHIC
    finally:
        Path(fname).unlink()


def test_xarray_accessor_tiled_grid_slice_and_add():
    """
    Check that the accessor works to get the registration and gtype when the grid source
    file is from a tiled grid, that slicing doesn't affect registration/gtype, but math
    operations do return the default registration/gtype as a fallback.

    Unit test to track https://github.com/GenericMappingTools/pygmt/issues/524
    """
    # Load the 05m earth relief grid, which is stored as tiles.
    grid = load_earth_relief(
        resolution="05m", region=[0, 5, -5, 5], registration="pixel"
    )
    # Registration and gtype are correct.
    assert grid.gmt.registration is GridRegistration.PIXEL
    assert grid.gmt.gtype is GridType.GEOGRAPHIC
    # The source grid file for tiled grids is the first tile
    assert grid.encoding["source"].endswith("S90E000.earth_relief_05m_p.nc")

    # For a sliced grid, ensure we don't fallback to the default registration (gridline)
    # and gtype (cartesian), because the source grid file should still exist.
    sliced_grid = grid[1:3, 1:3]
    assert sliced_grid.encoding["source"].endswith("S90E000.earth_relief_05m_p.nc")
    assert sliced_grid.gmt.registration is GridRegistration.PIXEL
    assert sliced_grid.gmt.gtype is GridType.GEOGRAPHIC

    # For a grid that underwent mathematical operations, fallback to default
    # registration and gtype, because the source grid file doesn't exist.
    added_grid = sliced_grid + 9
    assert added_grid.encoding == {}
    assert added_grid.gmt.registration is GridRegistration.GRIDLINE
    assert added_grid.gmt.gtype is GridType.CARTESIAN

    # Still possible to manually set registration and gtype.
    added_grid.gmt.registration = GridRegistration.PIXEL
    added_grid.gmt.gtype = GridType.GEOGRAPHIC
    assert added_grid.gmt.registration is GridRegistration.PIXEL
    assert added_grid.gmt.gtype is GridType.GEOGRAPHIC
