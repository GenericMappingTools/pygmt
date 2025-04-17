"""
Tests for xarray 'gmtread' backend engine.
"""

import xarray as xr
from pygmt.enums import GridRegistration, GridType


# %%
def test_xarray_backend_gmtread():
    """
    Ensure that passing engine='gmtread' to xarray.open_dataarray works.
    """
    with xr.open_dataarray(
        filename_or_obj="@static_earth_relief.nc", engine="gmtread"
    ) as da:
        assert da.sizes == {"lat": 14, "lon": 8}
        assert da.dtype == "float32"
        assert da.gmt.registration == GridRegistration.GRIDLINE
        assert da.gmt.gtype == GridType.CARTESIAN
