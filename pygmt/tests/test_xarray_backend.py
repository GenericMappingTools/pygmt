"""
Tests for xarray 'gmt' backend engine.
"""

import importlib
import re

import numpy as np
import numpy.testing as npt
import pytest
import xarray as xr
from pygmt.enums import GridRegistration, GridType
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile

_HAS_NETCDF4 = bool(importlib.util.find_spec("netCDF4"))


@pytest.mark.benchmark
@pytest.mark.skipif(condition=not _HAS_NETCDF4, reason="netCDF4 is not installed")
def test_xarray_backend_load_dataarray():
    """
    Check that xarray.load_dataarray works to read a netCDF grid with
    GMTDataArrayAccessor information loaded.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        rng = np.random.default_rng()
        grid = xr.DataArray(
            data=rng.random((2, 2)), coords=[[0.1, 0.2], [0.3, 0.4]], dims=("x", "y")
        )
        grid.to_netcdf(tmpfile.name)

        dataarray = xr.load_dataarray(tmpfile.name, engine="gmt", raster_kind="grid")

        assert dataarray.gmt.gtype is GridType.CARTESIAN
        assert dataarray.gmt.registration is GridRegistration.PIXEL
        # ensure data array can be saved back to a NetCDF file
        dataarray.to_netcdf(tmpfile.name)


def test_xarray_backend_gmt_open_nc_grid():
    """
    Ensure that passing engine='gmt' to xarray.open_dataarray works for opening NetCDF
    grids.
    """
    with xr.open_dataarray(
        "@static_earth_relief.nc", engine="gmt", raster_kind="grid"
    ) as da:
        assert da.sizes == {"lat": 14, "lon": 8}
        assert da.dtype == "float32"
        assert da.gmt.gtype is GridType.GEOGRAPHIC
        assert da.gmt.registration is GridRegistration.PIXEL


def test_xarray_backend_gmt_open_tif_image():
    """
    Ensure that passing engine='gmt' to xarray.open_dataarray works for opening GeoTIFF
    images.
    """
    with xr.open_dataarray("@earth_day_01d", engine="gmt", raster_kind="image") as da:
        assert da.sizes == {"band": 3, "y": 180, "x": 360}
        assert da.dtype == "uint8"
        assert da.gmt.gtype is GridType.GEOGRAPHIC
        assert da.gmt.registration is GridRegistration.PIXEL


def test_xarray_backend_gmt_load_grd_grid():
    """
    Ensure that passing engine='gmt' to xarray.load_dataarray works for loading GRD
    grids.
    """
    da = xr.load_dataarray(
        "@earth_relief_20m_holes.grd", engine="gmt", raster_kind="grid"
    )
    # Ensure data is in memory.
    assert isinstance(da.data, np.ndarray)
    npt.assert_allclose(da.min(), -4929.5)
    assert da.sizes == {"lat": 31, "lon": 31}
    assert da.dtype == "float32"
    assert da.gmt.gtype is GridType.GEOGRAPHIC
    assert da.gmt.registration is GridRegistration.GRIDLINE


def test_xarray_backend_gmt_read_invalid_kind():
    """
    Check that xarray.open_dataarray(..., engine="gmt") fails with missing or incorrect
    'raster_kind'.
    """
    with pytest.raises(
        TypeError,
        match=re.escape(
            "GMTBackendEntrypoint.open_dataset() missing 1 required keyword-only argument: 'raster_kind'"
        ),
    ):
        xr.open_dataarray("nokind.nc", engine="gmt")

    with pytest.raises(GMTInvalidInput):
        xr.open_dataarray(
            filename_or_obj="invalid.tif", engine="gmt", raster_kind="invalid"
        )
