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
import geopandas
import pygmt

# Read a sample dataset provided by Natural Earth. The dataset contains rivers stored
# as LineString/MultiLineString geometry types. Here will focus on Asia.
provider = "https://naciscdn.org/naturalearth"
rivers = geopandas.read_file(
    f"{provider}/50m/physical/ne_50m_rivers_lake_centerlines.zip"
)
rivers_asia = rivers.cx[57:125, 7:47].copy()

fig = pygmt.Figure()
fig.basemap(region=[57, 125, 7, 47], projection="M10c", frame=True)
fig.coast(land="gray95", shorelines="1/0.3p,gray50")

# Add rivers to map
fig.plot(data=rivers_asia, pen="1p,steelblue")

fig.show()
