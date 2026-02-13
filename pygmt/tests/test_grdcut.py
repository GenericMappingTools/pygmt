"""
Test pygmt.grdcut.
"""

import geopandas as gpd
import numpy as np
import pytest
import xarray as xr
from pygmt import grdcut
from pygmt.exceptions import GMTTypeError, GMTValueError
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import load_static_earth_relief
from shapely.geometry import MultiPolygon, Polygon


@pytest.fixture(scope="module", name="polygon")
def fixture_polygon():
    """
    Provide a reusable polygon geometry for grdcut tests.
    """
    return Polygon(
        [
            (-52.5, -19.5),
            (-51.5, -19.0),
            (-50.5, -18.5),
            (-51.5, -18.0),
            (-52.5, -19.5),
        ]
    )


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


def test_grdcut_dataarray_in_file_out(grid, expected_grid, region):
    """
    Test grdcut on an input DataArray, and output to a grid file.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdcut(grid, outgrid=tmpfile.name, region=region)
        assert result is None  # grdcut returns None if output to a file
        temp_grid = xr.load_dataarray(tmpfile.name, engine="gmt", raster_kind="grid")
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
    with pytest.raises(GMTTypeError):
        grdcut(np.arange(10).reshape((5, 2)))


def test_grdcut_invalid_kind(grid, region):
    """
    Check that grdcut fails with incorrect 'kind'.
    """
    with pytest.raises(GMTValueError):
        grdcut(grid, kind="invalid", region=region)


def test_grdcut_with_shapely_polygon(grid, polygon):
    """
    Grdcut should accept a shapely.geometry.Polygon as polygon input
    and produce a grid of expected size with some valid data.
    """
    outgrid = grdcut(grid=grid, polygon=polygon)
    assert outgrid is not None

    # Check size
    assert outgrid.size > 0

    # There should be some non-NaN pixels inside the polygon
    assert np.any(~np.isnan(outgrid.values))

    # Optionally, corners outside the polygon should be NaN
    corner_values = [
        outgrid.values[0, 0],
        outgrid.values[0, -1],
        outgrid.values[-1, 0],
        outgrid.values[-1, -1],
    ]
    assert any(np.isnan(val) for val in corner_values)


def test_grdcut_with_geodataframe_polygon(grid, polygon):
    """
    Grdcut should accept a geopandas.GeoDataFrame as polygon input
    and produce a grid of expected size with some valid data.
    """
    gdf = gpd.GeoDataFrame({"geometry": [polygon]}, crs="OGC:CRS84")
    outgrid = grdcut(grid=grid, polygon=gdf)
    assert outgrid is not None

    # Check size
    assert outgrid.size > 0

    # Some pixels should remain non-NaN
    assert np.any(~np.isnan(outgrid.values))


def test_grdcut_with_polygon_file(grid, tmp_path):
    """
    Grdcut should accept a GMT ASCII polygon file as polygon input.
    """
    gmtfile = tmp_path / "poly.gmt"
    gmtfile.write_text(
        ">\n-52.5 -19.5\n-51.5 -19.0\n-50.5 -18.5\n-51.5 -18.0\n-52.5 -19.5\n"
    )

    outgrid = grdcut(grid=grid, polygon=gmtfile)
    assert outgrid is not None
    assert outgrid.size > 0


@pytest.mark.parametrize(
    ("crop", "invert"), [(True, False), (False, True), (True, True)]
)
def test_grdcut_polygon_with_crop_and_invert(grid, polygon, crop, invert):
    """
    Grdcut should support crop (+c) and invert (+i) modifiers with polygon input.
    """
    gdf = gpd.GeoDataFrame({"geometry": [polygon]}, crs="OGC:CRS84")
    outgrid = grdcut(grid=grid, polygon=gdf, crop=crop, invert=invert)
    assert outgrid is not None
    assert outgrid.size > 0

    if invert:
        assert np.isnan(outgrid.data).any()

    assert np.isfinite(outgrid.data).any()

    assert np.count_nonzero(np.isfinite(outgrid.data)) < grid.size


def test_grdcut_with_multipolygon(grid):
    """
    Grdcut should accept a shapely.geometry.MultiPolygon as polygon input.
    """
    # Create two simple polygons and combine into a MultiPolygon
    poly1 = Polygon([(-52.5, -19.5), (-51.5, -19.0), (-50.5, -18.5), (-52.5, -19.5)])
    poly2 = Polygon([(-51.0, -18.5), (-50.5, -18.0), (-50.0, -18.5), (-51.0, -18.5)])
    multipoly = MultiPolygon([poly1, poly2])

    outgrid = grdcut(grid=grid, polygon=multipoly)
    assert outgrid is not None
    # Ensure some grid pixels exist
    assert outgrid.size > 0
    assert np.any(np.isnan(outgrid.values))


def test_grdcut_polygon_invalid_input(grid):
    """
    Grdcut should raise an error for invalid polygon input type.
    """
    with pytest.raises(GMTValueError):
        grdcut(grid=grid, polygon=12345)
