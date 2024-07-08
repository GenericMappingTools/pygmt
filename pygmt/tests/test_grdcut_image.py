"""
Test pygmt.grdcut on images.
"""

import pytest
import xarray as xr
from pygmt import grdcut, which

try:
    import rioxarray

    _HAS_RIOXARRAY = True
except ImportError:
    _HAS_RIOXARRAY = False


@pytest.mark.skipif(not _HAS_RIOXARRAY, reason="rioxarray is not installed")
def test_grdcut_image_file(region, expected_image):
    """
    Test grdcut on an input image file.
    """
    result = grdcut("@earth_day_01d", region=region)
    xr.testing.assert_allclose(a=result, b=expected_image)


@pytest.mark.skipif(not _HAS_RIOXARRAY, reason="rioxarray is not installed")
def test_grdcut_image_dataarray(region, expected_image):
    """
    Test grdcut on an input xarray.DataArray object.
    """
    path = which("@earth_day_01d", download="a")
    raster = rioxarray.open_rasterio(path)
    result = grdcut(raster, region=region)
    xr.testing.assert_allclose(a=result, b=expected_image)
