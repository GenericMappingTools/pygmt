"""
Tests for xarray 'gmt' backend engine.
"""

import re

import numpy as np
import pytest
import xarray as xr
from pygmt.enums import GridRegistration, GridType
from pygmt.exceptions import GMTInvalidInput


def test_xarray_backend_gmt_open_nc_grid():
    """
    Ensure that passing engine='gmt' to xarray.open_dataarray works for opening
    NetCDF grids.
    """
    with xr.open_dataarray(
        filename_or_obj="@static_earth_relief.nc", engine="gmt", decode_kind="grid"
    ) as da:
        assert da.sizes == {"lat": 14, "lon": 8}
        assert da.dtype == "float32"
        assert da.gmt.registration == GridRegistration.PIXEL
        assert da.gmt.gtype == GridType.GEOGRAPHIC


def test_xarray_backend_gmt_open_tif_image():
    """
    Ensure that passing engine='gmt' to xarray.open_dataarray works for opening
    GeoTIFF images.
    """
    with xr.open_dataarray(
        filename_or_obj="@earth_day_01d", engine="gmt", decode_kind="image"
    ) as da:
        assert da.sizes == {"band": 3, "y": 180, "x": 360}
        assert da.dtype == "uint8"
        assert da.gmt.registration == GridRegistration.PIXEL
        assert da.gmt.gtype == GridType.GEOGRAPHIC


def test_xarray_backend_gmt_load_grd_grid():
    """
    Ensure that passing engine='gmt' to xarray.open_dataarray works for loading
    GRD grids.
    """
    with xr.load_dataarray(
        filename_or_obj="@earth_relief_20m_holes.grd", engine="gmt", decode_kind="grid"
    ) as da:
        assert isinstance(
            da.data,
            np.ndarray,  # ensure data is in memory and not a dask array
        )
        assert da.sizes == {"lat": 31, "lon": 31}
        assert da.dtype == "float32"
        assert da.gmt.registration == GridRegistration.GRIDLINE
        assert da.gmt.gtype == GridType.GEOGRAPHIC


def test_xarray_backend_gmt_read_invalid_kind():
    """
    Check that xarray.open_dataarray(..., engine="gmt") fails with missing or incorrect
    'decode_kind'.
    """
    with pytest.raises(
        TypeError,
        match=re.escape(
            "GMTBackendEntrypoint.open_dataset() missing 1 required keyword-only argument: 'decode_kind'"
        ),
    ):
        xr.open_dataarray("nokind.nc", engine="gmt")

    with pytest.raises(GMTInvalidInput):
        xr.open_dataarray(
            filename_or_obj="invalid.tif", engine="gmt", decode_kind="invalid"
        )
