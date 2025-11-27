"""
GeoPandas: Plotting lines with LineString or MultiLineString geometry
=====================================================================

The :meth:`pygmt.Figure.plot` method allows us to plot geographical data such as lines
with LineString or MultiLineString geometry types stored in a
:class:`geopandas.GeoDataFrame` object. Use :func:`geopandas.read_file` to load data
from any supported OGR format such as a shapefile (.shp), GeoJSON (.geojson), geopackage
(.gpkg), etc. Then, pass the :class:`geopandas.GeoDataFrame` object as an argument to
the ``data`` parameter of :meth:`pygmt.Figure.plot`, and style the lines using the
``pen`` parameter.
"""

# %%
import geopandas as gpd
import pygmt

# Read a sample dataset provided by Natural Earth. The dataset contains rivers stored
# as LineString/MultiLineString geometry types. Here will focus on South America.
provider = "https://naciscdn.org/naturalearth"
rivers = gpd.read_file(f"{provider}/10m/physical/ne_10m_rivers_lake_centerlines.zip")

fig = pygmt.Figure()
fig.basemap(region=[-84.5, -33, -56.5, 13], projection="M10c", frame=True)
fig.coast(land="gray95", shorelines="1/0.3p,gray50", borders="1/0.2p,black")

# Add rivers to map
fig.plot(data=rivers, pen="1p,steelblue")

fig.show()

# %%
fig = pygmt.Figure()
fig.basemap(region=[-10, 30, 35, 57], projection="M10c", frame=True)
fig.coast(land="gray95", shorelines="1/0.3p,gray50", borders="1/0.1p,black")

# Add rivers to map
fig.plot(data=rivers, pen="1p,steelblue")

fig.show()
