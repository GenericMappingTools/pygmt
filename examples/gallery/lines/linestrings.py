# ruff: noqa: RUF003
"""
Plotting lines with LineString/MultiLineString geometry
=====

The :meth:`pygmt.Figure.plot` method allows us to plot geographical data such
as lines which are stored in a :class:`geopandas.GeoDataFrame` object. Use
:func:`geopandas.read_file` to load data from any supported OGR format such as
a shapefile (.shp), GeoJSON (.geojson), geopackage (.gpkg), etc. Then, pass the
:class:`geopandas.GeoDataFrame` as an argument to the ``data`` parameter of
:meth:`pygmt.Figure.plot`, and style the geometry using the ``pen`` parameter.
"""

# %%
import geopandas as gpd
import pygmt

# Read shapefile data using geopandas
gpd_lines = gpd.read_file(
    "https://www.eea.europa.eu/data-and-maps/data/wise-large-rivers-and-large-lakes/zipped-shapefile-with-wise-large-rivers-vector-line/zipped-shapefile-with-wise-large-rivers-vector-line/at_download/file/wise_large_rivers.zip"
)

# Convert object to EPSG 4326 coordinate system
gpd_lines_new = gpd_lines.to_crs("EPSG:4326")

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
fig.plot(data=gpd_lines_new, pen="1p,steelblue")

fig.show()