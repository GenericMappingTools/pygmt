"""
Choropleth map
==============

The :meth:`pygmt.Figure.choropleth` method allows us to plot geographical data such as
polygons which are stored in a :class:`geopandas.GeoDataFrame` object or a OGR_GMT file.
Use :func:`geopandas.read_file` to load data from any supported OGR formats such as a
shapefile (.shp), GeoJSON (.geojson), geopackage (.gpkg), etc. You can also use a full
URL pointing to your desired data source. Then, pass the :class:`geopandas.GeoDataFrame`
as an argument to the ``data`` parameter of :meth:`pygmt.Figure.choropleth`, and style
the geometry using the ``pen`` parameter. To fill the polygons based on a corresponding
column you need to specify the colum name to the ``column`` parameter.
"""

# %%
import geodatasets
import geopandas as gpd
import pygmt

# Read the example dataset provided by geodatasets.
gdf = gpd.read_file(geodatasets.get_path("geoda airbnb"))
print(gdf.head())

# %%
fig = pygmt.Figure()

fig.basemap(
    region=gdf.total_bounds[[0, 2, 1, 3]],
    projection="M6c",
    frame="+tPopulation of Chicago",
)

# The dataset contains different attributes, here we select the "population" column to
# plot.

# First, we define the colormap to fill the polygons based on the "population" column.
pygmt.makecpt(
    cmap="acton",
    series=[gdf["population"].min(), gdf["population"].max(), 10],
    continuous=True,
    reverse=True,
)

# Next, we plot the polygons and fill them using the defined colormap. The target column
# is specified by the `column` parameter.
fig.choropleth(data=gdf, column="population", pen="0.3p,gray10", cmap=True)

# Add colorbar legend.
fig.colorbar(frame="x+lPopulation", position="jML+o-0.5c+w3.5c/0.2c")

fig.show()
