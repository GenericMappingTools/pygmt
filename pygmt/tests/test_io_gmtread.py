"""
Test the gmtread function.
"""

import importlib

import numpy as np
import pytest
import rioxarray
import xarray as xr
from pygmt import gmtread, which

_HAS_NETCDF4 = bool(importlib.util.find_spec("netCDF4"))
_HAS_RIORASTERIO = bool(importlib.util.find_spec("rioxarray"))


@pytest.mark.skipif(not _HAS_NETCDF4, reason="netCDF4 is not installed.")
def test_io_gmtread_grid():
    """
    Test that reading a grid returns an xr.DataArray and the grid is the same as the one
    loaded via xarray.load_dataarray.
    """
    grid = gmtread("@static_earth_relief.nc", kind="grid")
    assert isinstance(grid, xr.DataArray)
    expected_grid = xr.load_dataarray(which("@static_earth_relief.nc", download="a"))
    assert np.allclose(grid, expected_grid)


@pytest.mark.skipif(not _HAS_RIORASTERIO, reason="rioxarray is not installed.")
def test_io_gmtread_image():
    """
    Test that reading an image returns an xr.DataArray.
    """
    image = gmtread("@earth_day_01d", kind="image")
    assert isinstance(image, xr.DataArray)
    with rioxarray.open_rasterio(
        which("@earth_day_01d", download="a")
    ) as expected_image:
        assert np.allclose(image, expected_image)


def test_io_gmtread_invalid_kind():
    """
    Test that an invalid kind raises a ValueError.
    """
    with pytest.raises(ValueError, match="Invalid kind"):
        gmtread("file.cpt", kind="cpt")


def test_io_gmtread_invalid_arguments():
    """
    Test that invalid arguments raise a ValueError for non-'dataset' kind.
    """
    with pytest.raises(ValueError, match="Only the 'dataset' kind supports"):
        gmtread("file.nc", kind="grid", column_names="foo")

    with pytest.raises(ValueError, match="Only the 'dataset' kind supports"):
        gmtread("file.nc", kind="grid", header=1)

    with pytest.raises(ValueError, match="Only the 'dataset' kind supports"):
        gmtread("file.nc", kind="grid", dtype="float")
