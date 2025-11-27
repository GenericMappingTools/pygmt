"""
Choropleth map
==============

The :meth:`pygmt.Figure.plot` method allows us to plot geographical data such as
polygons which are stored in a :class:`geopandas.GeoDataFrame` object. Use
:func:`geopandas.read_file` to load data from any supported OGR format such as a
shapefile (.shp), GeoJSON (.geojson), geopackage (.gpkg), etc. You can also use a full
URL pointing to your desired data source. Then, pass the :class:`geopandas.GeoDataFrame`
as an argument to the ``data`` parameter of :meth:`pygmt.Figure.plot`, and style the
geometry using the ``pen`` parameter. To fill the polygons based on a corresponding
column you need to set ``fill="+z"`` as well as select the appropriate column using the
``aspatial`` parameter as shown in the example below.
"""

# %%
import geopandas as gpd
import pygmt

provider = "https://naciscdn.org/naturalearth"
world = gpd.read_file(f"{provider}/50m/cultural/ne_50m_admin_0_countries.zip")

# The dataset contains different attributes, here we focus on the population within
# the different countries (column "POP_EST").
world["POP_EST"] *= 1e-6

fig = pygmt.Figure()
fig.basemap(region=[-19.5, 53, -37.5, 38], projection="M15c", frame="+n")

# First, we define the colormap to fill the polygons based on the "POP_EST" column.
pygmt.makecpt(cmap="acton", series=(0, 100), reverse=True)

# Next, we plot the polygons and fill them using the defined colormap. The target column
# is defined by the aspatial parameter.
fig.plot(
    data=world[world["CONTINENT"] == "Africa"].copy(),
    pen="1p,gray50",
    fill="+z",
    cmap=True,
    aspatial="Z=POP_EST",
)

# Add colorbar legend.
fig.colorbar(
    frame="x10f5+lPopulation (millions)",
    position="jML+o3c/-3.5c+w7.5c+ef0.3c+ml",
)

fig.show()
