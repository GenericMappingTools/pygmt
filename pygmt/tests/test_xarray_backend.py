"""
Tests for xarray 'gmt' backend engine.
"""

import importlib

import numpy as np
import numpy.testing as npt
import pytest
import xarray as xr
from pygmt.clib import Session
from pygmt.enums import GridRegistration, GridType
from pygmt.exceptions import GMTValueError
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


def test_xarray_backend_load_dataarray_temp_nc_grid():
    """
    Check that xarray.load_dataarray works to read a temporary netCDF grid, and ensure
    that GMTDataArrayAccessor information is retained after original file is deleted.

    This is a regression test for
    https://github.com/GenericMappingTools/pygmt/issues/4005
    """

    with Session() as lib:
        with GMTTempFile(suffix=".nc") as tmpfile:
            args = [
                "@earth_relief_01d_g",
                "-T",  # change from gridline to pixel registration
                f"-G{tmpfile.name}",
            ]
            lib.call_module(module="grdedit", args=args)
            dataarray = xr.load_dataarray(
                tmpfile.name, engine="gmt", raster_kind="grid"
            )

        # Ensure GMTDataArrayAccessor info is preserved after tempfile is deleted
        assert dataarray.gmt.registration is GridRegistration.PIXEL
        assert dataarray.gmt.gtype is GridType.CARTESIAN


def test_xarray_backend_gmt_open_nc_grid():
    """
    Ensure that passing engine='gmt' to xarray.open_dataarray works to open a netCDF
    grid.
    """
    with xr.open_dataarray(
        "@static_earth_relief.nc", engine="gmt", raster_kind="grid"
    ) as da:
        assert da.sizes == {"lat": 14, "lon": 8}
        assert da.dtype == "float32"
        assert da.gmt.gtype is GridType.GEOGRAPHIC
        assert da.gmt.registration is GridRegistration.PIXEL


def test_xarray_backend_gmt_open_nc_grid_with_region_bbox():
    """
    Ensure that passing engine='gmt' with a `region` argument to xarray.open_dataarray
    works to open a netCDF grid over a specific bounding box.
    """
    with xr.open_dataarray(
        "@static_earth_relief.nc",
        engine="gmt",
        raster_kind="grid",
        region=[-52, -48, -18, -12],
    ) as da:
        assert da.sizes == {"lat": 6, "lon": 4}
        npt.assert_allclose(da.lat, [-17.5, -16.5, -15.5, -14.5, -13.5, -12.5])
        npt.assert_allclose(da.lon, [-51.5, -50.5, -49.5, -48.5])
        assert da.dtype == "float32"
        assert da.gmt.gtype is GridType.GEOGRAPHIC
        assert da.gmt.registration is GridRegistration.PIXEL


def test_xarray_backend_gmt_open_tif_image():
    """
    Ensure that passing engine='gmt' to xarray.open_dataarray works to open a GeoTIFF
    image.
    """
    with xr.open_dataarray("@earth_day_01d", engine="gmt", raster_kind="image") as da:
        assert da.sizes == {"band": 3, "y": 180, "x": 360}
        assert da.dtype == "uint8"
        assert da.gmt.gtype is GridType.GEOGRAPHIC
        assert da.gmt.registration is GridRegistration.PIXEL


def test_xarray_backend_gmt_open_tif_image_with_region_iso():
    """
    Ensure that passing engine='gmt' with a `region` argument to xarray.open_dataarray
    works to open a GeoTIFF image over a specific ISO country code border.
    """
    with xr.open_dataarray(
        "@earth_day_01d", engine="gmt", raster_kind="image", region="BN"
    ) as da:
        assert da.sizes == {"band": 3, "lat": 2, "lon": 2}
        npt.assert_allclose(da.lat, [5.5, 4.5])
        npt.assert_allclose(da.lon, [114.5, 115.5])
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
    with pytest.raises(TypeError, match=r"missing a required argument: 'raster_kind'"):
        xr.open_dataarray("nokind.nc", engine="gmt")

    with pytest.raises(GMTValueError):
        xr.open_dataarray(
            filename_or_obj="invalid.tif", engine="gmt", raster_kind="invalid"
        )
