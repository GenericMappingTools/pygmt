"""
GeoPandas: Plotting lines with LineString or MultiLineString geometry
=====================================================================

The :meth:`pygmt.Figure.plot` method allows us to plot geographical data such as lines
with LineString or MultiLineString geometry types stored in a
:class:`geopandas.GeoDataFrame` object or any object that implements the
`__geo_interface__ <https://gist.github.com/sgillies/2217756>`__ property.

Use :func:`geopandas.read_file` to load data from any supported OGR format such as a
shapefile (.shp), GeoJSON (.geojson), geopackage (.gpkg), etc. Then, pass the
:class:`geopandas.GeoDataFrame` object as an argument to the ``data`` parameter of
:meth:`pygmt.Figure.plot`, and style the lines using the ``pen`` parameter.
"""

# %%
import geodatasets
import geopandas as gpd
import pygmt

# Read a sample dataset provided by the geodatasets package.
# The dataset contains large rivers in Europe, stored as LineString/MultiLineString
# geometry types.
gdf = gpd.read_file(geodatasets.get_path("eea large_rivers"))

# Convert object to EPSG 4326 coordinate system
gdf = gdf.to_crs("EPSG:4326")
gdf.head()

# %%
fig = pygmt.Figure()

fig.coast(
    projection="M10c",
    region=[-10, 30, 35, 57],
    resolution="l",
    land="gray95",
    shorelines="1/0.1p,gray50",
    borders="1/0.1,gray30",
    frame=True,
)

# Add rivers to map
fig.plot(data=gdf, pen="1p,steelblue")

fig.show()
