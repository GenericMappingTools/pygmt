"""
Tests for input/output (I/O) utilities.
"""
import numpy as np
import pytest
import xarray as xr
from pygmt.helpers import GMTTempFile
from pygmt.io import load_dataarray


def test_io_load_dataarray():
    """
    Check that load_dataarray works to read a NetCDF grid with
    GMTDataArrayAccessor information loaded.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        grid = xr.DataArray(
            data=np.random.rand(2, 2), coords=[[0.1, 0.2], [0.3, 0.4]], dims=("x", "y")
        )
        grid.to_netcdf(tmpfile.name)
        dataarray = load_dataarray(tmpfile.name)
        assert dataarray.gmt.gtype == 0  # Cartesian grid
        assert dataarray.gmt.registration == 1  # Pixel registration
        # this would fail if we used xr.open_dataarray instead of
        # load_dataarray
        dataarray.to_netcdf(tmpfile.name)


def test_io_load_dataarray_cache():
    """
    Check that load_dataarray fails when the cache argument is used.
    """
    with pytest.raises(TypeError):
        _ = load_dataarray("somefile.nc", cache=True)
