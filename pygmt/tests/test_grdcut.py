"""
Test pygmt.grdcut.
"""

import numpy as np
import pytest
import xarray as xr
from pygmt import grdcut, load_dataarray, which
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import load_static_earth_relief

try:
    import rioxarray

    _HAS_RIOXARRAY = True
except ImportError:
    _HAS_RIOXARRAY = False


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_static_earth_relief()


@pytest.fixture(scope="module", name="region")
def fixture_region():
    """
    Set the data region.
    """
    return [-53, -49, -20, -17]


@pytest.fixture(scope="module", name="expected_grid")
def fixture_expected_grid():
    """
    Load the expected grdcut grid result.
    """
    return xr.DataArray(
        data=[
            [446.5, 481.5, 439.5, 553.0],
            [757.0, 570.5, 538.5, 524.0],
            [796.0, 886.0, 571.5, 638.5],
        ],
        coords={"lon": [-52.5, -51.5, -50.5, -49.5], "lat": [-19.5, -18.5, -17.5]},
        dims=["lat", "lon"],
    )


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
            "spatial_ref": 0,
        },
        dims=["band", "y", "x"],
        attrs={
            "scale_factor": 1.0,
            "add_offset": 0.0,
            "_FillValue": 0,
            "STATISTICS_MAXIMUM": 95,
            "STATISTICS_MEAN": 90.91666666666667,
            "STATISTICS_MINIMUM": 89,
            "STATISTICS_STDDEV": 1.5523280008498,
            "STATISTICS_VALID_PERCENT": 100,
            "AREA_OR_POINT": "Area",
        },
    )


def test_grdcut_dataarray_in_file_out(grid, expected_grid, region):
    """
    Test grdcut on an input DataArray, and output to a grid file.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdcut(grid, outgrid=tmpfile.name, region=region)
        assert result is None  # grdcut returns None if output to a file
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


@pytest.mark.benchmark
def test_grdcut_dataarray_in_dataarray_out(grid, expected_grid, region):
    """
    Test grdcut on an input DataArray, and output as DataArray.
    """
    outgrid = grdcut(grid, region=region)
    assert isinstance(outgrid, xr.DataArray)
    xr.testing.assert_allclose(a=outgrid, b=expected_grid)


def test_grdcut_fails():
    """
    Check that grdcut fails correctly.
    """
    with pytest.raises(GMTInvalidInput):
        grdcut(np.arange(10).reshape((5, 2)))


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
    with rioxarray.open_rasterio(path) as raster:
        result = grdcut(raster, region=region)
    xr.testing.assert_allclose(a=result, b=expected_image)
