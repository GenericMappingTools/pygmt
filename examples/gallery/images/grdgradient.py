"""
Calculating the gradient of a grid file
--------------------
The :meth:`pygmt.grgradient` calculate the gradient of a grid file.
In the example shown below we will see how to calculate an hillshade map based on
a Data Elevation Model(DEM). :meth:`pygmt.grdgradient` get as input :class:`xarray.DataArray` object
or a path string to a grid file. We will use the ``radiance`` parameter in order to set the illumination
source direction and altitude
"""

import pygmt

fig = pygmt.Figure()

# Define region of interest around Yosemite valley
region = [-119.825, -119.4, 37.6, 37.825]

# Load sample grid (3 arc second global relief) in target area
grid = pygmt.datasets.load_earth_relief(resolution="03s", region=region)

# calculate the reflection of a light source projecting from west to east(azimuth 270)
# and at a latitude of 30 degrees from the horizon
dgrid = pygmt.grdgradient(grid=grid, radiance=[270, 30])

fig = pygmt.Figure()
# define figure configuration
pygmt.config(FORMAT_GEO_MAP="ddd.x", MAP_FRAME_TYPE="plain")

# --------------- plotting the hillshade map -----------
pygmt.makecpt(cmap="gray", series=[-1.5, 0.3, 0.01])
fig.grdimage(
    grid=dgrid,
    projection="M12c",
    frame=['WSrt+t"Hillshaded Map"', "xa0.1", "ya0.1"],
    cmap=True,
    region=region,
)

# Shift plot origin of the second map by "width of the first map + 0.5 cm"
# in x direction
fig.shift_origin(xshift="w+0.5c")

# --------------- plotting the original Data Elevation Model -----------

pygmt.makecpt(cmap="gray", series=[200, 4000, 10])
fig.grdimage(
    grid=grid,
    projection="M12c",
    frame=['lSrt+t"Original Data Elevation Model"', "xa0.1", "ya0.1"],
    cmap=True,
    region=region,
)
fig.colorbar(position="JMR+o0.4c/0c+w7c/0.5c+mc", frame=["xa1000f500", "y+lm"])
fig.show()
