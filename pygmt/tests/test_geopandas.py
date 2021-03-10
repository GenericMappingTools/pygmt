"""
Tests on integration with geopandas.
"""
import numpy.testing as npt
import pytest
from pygmt import info

gpd = pytest.importorskip("geopandas")
shapely = pytest.importorskip("shapely")


@pytest.fixture(scope="module", name="gdf")
def fixture_gdf():
    """
    Create a sample geopandas GeoDataFrame object with shapely geometries of
    different types.
    """
    linestring = shapely.geometry.LineString([(20, 15), (30, 15)])
    polygon = shapely.geometry.Polygon([(20, 10), (23, 10), (23, 14), (20, 14)])
    multipolygon = shapely.geometry.shape(
        {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [[0, 0], [20, 0], [10, 20], [0, 0]],  # Counter-clockwise
                    [[3, 2], [10, 16], [17, 2], [3, 2]],  # Clockwise
                ],
                [[[6, 4], [14, 4], [10, 12], [6, 4]]],  # Counter-clockwise
                [[[25, 5], [30, 10], [35, 5], [25, 5]]],
            ],
        }
    )
    # Multipolygon first so the OGR_GMT file has @GMULTIPOLYGON in the header
    gdf = gpd.GeoDataFrame(
        index=["multipolygon", "polygon", "linestring"],
        geometry=[multipolygon, polygon, linestring],
    )

    return gdf


def test_geopandas_info_geodataframe(gdf):
    """
    Check that info can return the bounding box region from a
    geopandas.GeoDataFrame.
    """
    output = info(table=gdf, per_column=True)
    npt.assert_allclose(actual=output, desired=[0.0, 35.0, 0.0, 20.0])


@pytest.mark.parametrize(
    "geomtype,desired",
    [
        ("multipolygon", [0.0, 35.0, 0.0, 20.0]),
        ("polygon", [20.0, 23.0, 10.0, 14.0]),
        ("linestring", [20.0, 30.0, 15.0, 15.0]),
    ],
)
def test_geopandas_info_shapely(gdf, geomtype, desired):
    """
    Check that info can return the bounding box region from a shapely.geometry
    object that has a __geo_interface__ property.
    """
    geom = gdf.loc[geomtype].geometry
    output = info(table=geom, per_column=True)
    npt.assert_allclose(actual=output, desired=desired)
