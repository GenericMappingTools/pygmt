"""
Filled polygons
===============

The :meth:`pygmt.Figure.plot` method allows us to plot geographical data such
as polygons which are stored in a :class:`geopandas.GeoDataFrame` object. Use
:func:`geopandas.read_file` to load data from any supported OGR format such as
a shapefile (.shp), GeoJSON (.geojson), geopackage (.gpkg), etc. You can also
use a full URL pointing to your desired data source. Then, pass the
:class:`geopandas.GeoDataFrame` as an argument to the ``data`` parameter in
:meth:`pygmt.Figure.plot`, and style the geometry using the ``pen`` parameter.
To fill the polygons based on a corresponding column you need to set
``fill="+z"```as well as select the appropriate column using the ``aspatial``
parameter as shown in the example below.
"""

import geopandas as gpd
import numpy as np
import pygmt

# Read polygon data using geopandas
gdf = gpd.read_file("https://geodacenter.github.io/data-and-lab//data/airbnb.zip")
# Automatically get min/max coordinates of polygon set
bounds = gdf.total_bounds
# Define an edge in degrees to add in each direction to the min/max coordinates
edge = 0.02

fig = pygmt.Figure()

fig.coast(
    region=[bounds[0] - edge, bounds[2] + edge, bounds[1] - edge, bounds[3] + edge],
    projection="M10c",
    frame=["af", "+tPopulation of Chicago"],
    water="lightblue",
    land="gray70",
    shorelines="1/1p,gray70",
)

# The dataset contains different parameters, here we select
# the "population" column to plot.

# First, we define the colormap to fill the polygons based on
# only the "population" column.
pygmt.makecpt(
    cmap="acton",
    series=[np.min(gdf["population"]), np.max(gdf["population"]), 10],
    continuous=True,
    reverse=True,
)

# Next, we plot the polygons and fill them using the defined
# colormap. The target column is defined by the aspatial
# parameter.
fig.plot(
    data=gdf[["population", "geometry"]],
    pen="0.3p,gray10",
    close=True,
    fill="+z",
    cmap=True,
    aspatial="Z=population",
)


# Add colorbar legend
fig.colorbar(frame="x+lPopulation")

fig.show()
