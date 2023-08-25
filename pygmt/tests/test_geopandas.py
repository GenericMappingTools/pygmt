"""
Test integration with geopandas.
"""
import numpy.testing as npt
import pytest
from pygmt import Figure, info, makecpt, which

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
    output = info(data=gdf, per_column=True)
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
    output = info(data=geom, per_column=True)
    npt.assert_allclose(actual=output, desired=desired)


@pytest.mark.mpl_image_compare
def test_geopandas_plot_default_square():
    """
    Check the default behavior of plotting a geopandas DataFrame with Point
    geometry in 2d.
    """
    point = shapely.geometry.Point(1, 2)
    gdf = gpd.GeoDataFrame(geometry=[point])
    fig = Figure()
    fig.plot(data=gdf, region=[0, 2, 1, 3], projection="X2c", frame=True)
    return fig


@pytest.mark.mpl_image_compare
def test_geopandas_plot3d_default_cube():
    """
    Check the default behavior of plotting a geopandas DataFrame with
    MultiPoint geometry in 3d.
    """
    multipoint = shapely.geometry.MultiPoint([(0.5, 0.5, 0.5), (1.5, 1.5, 1.5)])
    gdf = gpd.GeoDataFrame(geometry=[multipoint])
    fig = Figure()
    fig.plot3d(
        data=gdf,
        perspective=[315, 25],
        region=[0, 2, 0, 2, 0, 2],
        projection="X2c",
        frame=["WsNeZ1", "xag", "yag", "zag"],
        zscale=1.5,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_geopandas_plot_non_default_circle():
    """
    Check the default behavior of plotting geopandas DataFrame with Point
    geometry in 2d.
    """
    point = shapely.geometry.Point(1, 2)
    gdf = gpd.GeoDataFrame(geometry=[point])
    fig = Figure()
    fig.plot(data=gdf, region=[0, 2, 1, 3], projection="X2c", frame=True, style="c0.2c")
    return fig


@pytest.mark.mpl_image_compare
def test_geopandas_plot3d_non_default_circle():
    """
    Check the default behavior of plotting geopandas DataFrame with MultiPoint
    geometry in 3d.
    """
    multipoint = shapely.geometry.MultiPoint([(0.5, 0.5, 0.5), (1.5, 1.5, 1.5)])
    gdf = gpd.GeoDataFrame(geometry=[multipoint])
    fig = Figure()
    fig.plot3d(
        data=gdf,
        perspective=[315, 25],
        region=[0, 2, 0, 2, 0, 2],
        projection="X2c",
        frame=["WsNeZ1", "xag", "yag", "zag"],
        zscale=1.5,
        style="c0.2c",
    )
    return fig


@pytest.mark.parametrize(
    "dtype",
    [
        "int32",
        "int64",
        # Enable Int32/Int64 dtypes when geopandas>=0.13.3 is released with
        # patch https://github.com/geopandas/geopandas/pull/2950
        # pd.Int32Dtype(),
        # pd.Int64Dtype(),
    ],
)
@pytest.mark.mpl_image_compare(filename="test_geopandas_plot_int_dtypes.png")
def test_geopandas_plot_int_dtypes(dtype):
    """
    Check that plotting a geopandas GeoDataFrame with integer columns works,
    including int32 and int64 (non-nullable), Int32 and Int64 (nullable).

    This is a regression test for
    https://github.com/GenericMappingTools/pygmt/issues/2497
    """
    # Read shapefile in geopandas.GeoDataFrame
    shapefile = which(
        fname="@RidgeTest.shp @RidgeTest.shx @RidgeTest.dbf @RidgeTest.prj",
        download="c",
    )
    gdf = gpd.read_file(shapefile[0])

    # Reproject geometry and change dtype of NPOINTS column
    gdf["geometry"] = (
        gdf.to_crs(crs="EPSG:3857")
        .buffer(distance=100000)
        .to_crs(crs="OGC:CRS84")  # convert to lon/lat to prevent @null in PROJ CRS
    )
    gdf["NPOINTS"] = gdf.NPOINTS.astype(dtype=dtype)

    # Plot figure with three polygons colored based on NPOINTS value
    fig = Figure()
    makecpt(cmap="lisbon", series=[10, 60, 10], continuous=True)
    fig.plot(
        data=gdf,
        frame=True,
        pen="1p,black",
        close=True,
        fill="+z",
        cmap=True,
        aspatial="Z=NPOINTS",
    )
    fig.colorbar()
    return fig
