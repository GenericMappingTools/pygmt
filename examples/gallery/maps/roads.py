"""
Roads 
--------------------
The :meth:`pygmt.Figure.plot` method allows to plot geographical data which is
stored in a geopandas.GeoDataFrame object.
"""

import geopandas as gpd
import pygmt

# read shapefile data using geopandas
gdf = gpd.read_file(
    "http://www2.census.gov/geo/tiger/TIGER2015/PRISECROADS/tl_2015_15_prisecroads.zip"
)

# the dataset contains different road types listed in the RTTYP column,
# here we select the following ones to plot:
# Common name roads
roads_common = gdf[df.RTTYP == "M"]
# State recognized roads
roads_state = gdf[df.RTTYP == "S"]
# Interstates
roads_interstate = gdf[df.RTTYP == "I"]

fig = pygmt.Figure()

# Define target region around O'ahu (Hawai'i)
region = [-158.3, -157.6, 21.2, 21.75]

fig.basemap(region=region, projection="M12c", frame=True)
fig.coast(land="gray", water="dodgerblue4", shorelines="1p,black")

# Plot the individual road types with different pen settings and assgin labels which are
# displayed in the legend
fig.plot(data=roads_common, pen="5p,dodgerblue", label="CommonName")
fig.plot(data=roads_state, pen="2p,gold", label="StateRecognized")
fig.plot(data=roads_interstate, pen="2p,red", label="Interstate")

# Add legend
fig.legend()

fig.show()
