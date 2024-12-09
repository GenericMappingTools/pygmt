"""
Test pygmt.grdcut on images.
"""

from pathlib import Path

import numpy as np
import pytest
import xarray as xr
from pygmt import grdcut
from pygmt.datasets import load_blue_marble
from pygmt.helpers import GMTTempFile

try:
    import rioxarray

    _HAS_RIOXARRAY = True
except ImportError:
    _HAS_RIOXARRAY = False


@pytest.fixture(scope="module", name="region")
def fixture_region():
    """
    Set the data region.
    """
    return [-53, -49, -20, -17]


@pytest.fixture(scope="module", name="expected_image")
def fixture_expected_image():
    """
    Load the expected grdcut image result.
    """
    return xr.DataArray(
        data=np.array(
            [
                [[90, 93, 95, 90], [91, 90, 91, 91], [91, 90, 89, 90]],
                [[87, 88, 88, 89], [88, 87, 86, 85], [90, 90, 89, 88]],
                [[48, 49, 49, 45], [49, 48, 47, 45], [48, 47, 48, 46]],
            ],
            dtype=np.uint8,
        ),
        coords={
            "band": [1, 2, 3],
            "x": [-52.5, -51.5, -50.5, -49.5],
            "y": [-17.5, -18.5, -19.5],
        },
        dims=["band", "y", "x"],
        attrs={
            "scale_factor": 1.0,
            "add_offset": 0.0,
        },
    )


@pytest.mark.benchmark
def test_grdcut_image_file(region, expected_image):
    """
    Test grdcut on an input image file.
    """
    result = grdcut("@earth_day_01d", region=region, kind="image")
    xr.testing.assert_allclose(a=result, b=expected_image)


@pytest.mark.benchmark
@pytest.mark.skipif(not _HAS_RIOXARRAY, reason="rioxarray is not installed")
def test_grdcut_image_dataarray(region, expected_image):
    """
    Test grdcut on an input xarray.DataArray object.
    """
    raster = load_blue_marble()
    result = grdcut(raster, region=region, kind="image")
    xr.testing.assert_allclose(a=result, b=expected_image)


def test_grdcut_image_file_in_file_out(region, expected_image):
    """
    Test grdcut on an input image file and outputs to another image file.
    """
    with GMTTempFile(suffix=".tif") as tmp:
        result = grdcut("@earth_day_01d", region=region, outgrid=tmp.name)
        assert result is None
        assert Path(tmp.name).stat().st_size > 0
        if _HAS_RIOXARRAY:
            with rioxarray.open_rasterio(tmp.name) as raster:
                image = raster.load().drop_vars("spatial_ref")
                xr.testing.assert_allclose(a=image, b=expected_image)
