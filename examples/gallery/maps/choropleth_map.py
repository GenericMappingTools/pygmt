"""
Choropleth map
==============

The :meth:`pygmt.Figure.choropleth` method allows us to plot geographical data such as
polygons which are stored in a :class:`geopandas.GeoDataFrame` object or an OGR_GMT file.
Use :func:`geopandas.read_file` to load data from any supported OGR formats such as a
shapefile (.shp), GeoJSON (.geojson), geopackage (.gpkg), etc. You can also use a full
URL pointing to your desired data source. Then, pass the :class:`geopandas.GeoDataFrame`
as an argument to the ``data`` parameter of :meth:`pygmt.Figure.choropleth`, and style
the geometry using the ``pen`` parameter. To fill the polygons based on a corresponding
column you need to specify the column name to the ``column`` parameter.
"""

# %%
import geopandas as gpd
import pygmt
from pygmt.params.position import Position

provider = "https://naciscdn.org/naturalearth"
world = gpd.read_file(f"{provider}/110m/cultural/ne_110m_admin_0_countries.zip")

# The dataset contains different attributes, here we focus on the population within
# the different countries (column "POP_EST") for the continent "Africa".
world["POP_EST"] *= 1e-6
africa = world[world["CONTINENT"] == "Africa"].copy()

fig = pygmt.Figure()
fig.basemap(region=[-19.5, 53, -37.5, 38], projection="M10c", frame="+n")

# First, we define the colormap to fill the polygons based on the "POP_EST" column.
pygmt.makecpt(cmap="SCM/acton", series=(0, 100), reverse=True)

# Next, we plot the polygons and fill them using the defined colormap. The target column
# is defined by the aspatial parameter.
fig.plot(data=africa, pen="0.8p,gray50", fill="+z", cmap=True, aspatial="Z=POP_EST")

# Add colorbar legend.
fig.colorbar(
    frame="x+lPopulation (millions)",
    position=Position("ML", offset=(2, -2.5)),
    length=5,
    fg_triangle=True,
    triangle_height=0.2,
    move_text="label",
)

<<<<<<< HEAD
=======
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

# Add colorbar legend
fig.colorbar(frame="x+lPopulation", position="jML+o-0.5c+w3.5c/0.2c")

>>>>>>> e5f21af07 (Add Figure.choropleth to plot choropleth maps)
fig.show()
