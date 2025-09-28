"""
Clipping grid to a complex polygon
==================================

The :func:`pygmt.grdcut` function allows you to extract a subregion from a
grid. In this example we use a complex polygon (GeoDataFrame or GMT ASCII file)
to crop the grid to a region of interest.
"""

# %%
import geopandas as gpd
import pygmt
from shapely.geometry import Polygon

fig = pygmt.Figure()

# Define region of interest around Iceland
region = [-28, -10, 62, 68]

# Load sample grid (3 arc-minutes global relief) in target area
grid = pygmt.datasets.load_earth_relief(resolution="03m", region=region)

# Plot original grid
fig.basemap(
    region=region,
    projection="M12c",
    frame=["WSne+toriginal grid", "xa5f1", "ya2f1"],
)
fig.grdimage(grid=grid, cmap="oleron")

# Shift plot origin of the second map by "width of the first map + 0.5 cm"
# in x-direction
fig.shift_origin(xshift="w+0.5c")

# Create a more complex polygon (irregular shape) around a smaller ROI
complex_poly = Polygon(
    [
        (-26, 63),
        (-23, 63.5),
        (-20, 64),
        (-18, 65),
        (-19, 66),
        (-22, 66.5),
        (-25, 66),
        (-27, 65),
        (-26, 63),
    ]
)
gdf = gpd.GeoDataFrame({"geometry": [complex_poly]}, crs="EPSG:4326")

# Crop the grid using the complex polygon
cropped_grid = pygmt.grdcut(grid=grid, polygon=gdf)

# Plot cropped grid
fig.basemap(
    region=region,
    projection="M12c",
    frame=["wSne+tpolygon cropped grid", "xa5f1", "ya2f1"],
)
fig.grdimage(grid=cropped_grid, cmap="oleron")
fig.colorbar(frame=["x+lElevation", "y+lm"], position="JMR+o0.5c/0c+w8c")

fig.show()
