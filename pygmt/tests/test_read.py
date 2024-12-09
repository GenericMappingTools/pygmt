"""
Test the read function.
"""

import importlib

import numpy as np
import pytest
import xarray as xr
from pygmt import read, which

_HAS_NETCDF4 = bool(importlib.util.find_spec("netCDF4"))


@pytest.mark.skipif(not _HAS_NETCDF4, reason="netCDF4 is not installed.")
def test_read_grid():
    """
    Test that reading a grid returns an xr.DataArray and the grid is the same as the one
    loaded via xarray.load_dataarray.
    """
    grid = read("@static_earth_relief.nc", kind="grid")
    assert isinstance(grid, xr.DataArray)
    expected_grid = xr.load_dataarray(which("@static_earth_relief.nc", download="a"))
    assert np.allclose(grid, expected_grid)


def test_read_invalid_kind():
    """
    Test that an invalid kind raises a ValueError.
    """
    with pytest.raises(ValueError, match="Invalid kind"):
        read("file.cpt", kind="cpt")


def test_read_invalid_arguments():
    """
    Test that invalid arguments raise a ValueError for non-'dataset' kind.
    """
    with pytest.raises(ValueError, match="Only the 'dataset' kind supports"):
        read("file.nc", kind="grid", column_names="foo")

    with pytest.raises(ValueError, match="Only the 'dataset' kind supports"):
        read("file.nc", kind="grid", header=1)

    with pytest.raises(ValueError, match="Only the 'dataset' kind supports"):
        read("file.nc", kind="grid", dtype="float")
