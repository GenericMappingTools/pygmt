# ruff: noqa: RUF003
"""
Rivers
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
    "https://www.eea.europa.eu/data-and-maps/data/wise-large-rivers-and-large-lakes/zipped-shapefile-with-wise-large-rivers-vector-line/zipped-shapefile-with-wise-large-rivers-vector-line/at_download/file/" + \
    "wise_large_rivers.zip"
)    






