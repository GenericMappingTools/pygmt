"""
Tests for xarray 'gmtread' backend engine.
"""

import pytest
import xarray as xr
from pygmt.enums import GridRegistration, GridType
from pygmt.exceptions import GMTInvalidInput


def test_xarray_backend_gmtread_grid():
    """
    Ensure that passing engine='gmtread' to xarray.open_dataarray works for reading
    NetCDF grids.
    """
    with xr.open_dataarray(
        filename_or_obj="@static_earth_relief.nc", engine="gmtread", decode_kind="grid"
    ) as da:
        assert da.sizes == {"lat": 14, "lon": 8}
        assert da.dtype == "float32"
        assert da.gmt.registration == GridRegistration.PIXEL
        assert da.gmt.gtype == GridType.GEOGRAPHIC


def test_xarray_backend_gmtread_image():
    """
    Ensure that passing engine='gmtread' to xarray.open_dataarray works for reading
    GeoTIFF images.
    """
    with xr.open_dataarray(
        filename_or_obj="@earth_day_01d", engine="gmtread", decode_kind="image"
    ) as da:
        assert da.sizes == {"band": 3, "y": 180, "x": 360}
        assert da.dtype == "uint8"
        assert da.gmt.registration == GridRegistration.PIXEL
        assert da.gmt.gtype == GridType.GEOGRAPHIC


def test_xarray_backend_gmtread_invalid_kind():
    """
    Check that xarray.open_dataarray(..., engine="gmtread") fails with missing or
    incorrect 'decode_kind'.
    """
    with pytest.raises(GMTInvalidInput):
        xr.open_dataarray("nokind.nc", engine="gmtread")

    with pytest.raises(GMTInvalidInput):
        xr.open_dataarray(
            filename_or_obj="invalid.tif", engine="gmtread", decode_kind="invalid"
        )
