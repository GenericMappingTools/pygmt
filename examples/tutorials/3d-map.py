"""
Creating a 3D map
=================

Plotting a three-dimensional map is handled by :meth:`pygmt.Figure.grdview`.
"""

import pygmt

# Load sample earth relief data
grid = pygmt.datasets.load_earth_relief(resolution="05m", region=[-108, -103, 35, 40])

########################################################################################
# The :meth:`pygmt.Figure.grdview` method takes the ``grid`` input.
# The ``perspective`` argument changes the azimuth and angle of the viewpoint; the
# default is [180, 90], which is looking directly down on the figure and north is "up".
# The ``zsize`` argument sets how tall the three-dimensional portion appears.
#
# The default figure surface is *mesh plot*.

fig = pygmt.Figure()
fig.grdview(
    grid=grid,
    # Sets the view azimuth as 180 degrees, and the view angle as 30 degrees
    perspective=[180, 30],
    # Sets the x- and y-axis labels, and annotates the west, south, and east axes
    frame=["xa", "ya", "WSnE"],
    # Sets a Mercator projection on a 15-centimeter figure
    projection="M15c",
    # Sets the height of the three-dimensional relief at 1.5 centimeters
    zsize="1.5c",
)
fig.show()

########################################################################################
# The figure surface type can be set with the ``surftype`` parameter.
# The default CPT is *turbo*.

fig = pygmt.Figure()
fig.grdview(
    grid=grid,
    perspective=[180, 30],
    frame=["xa", "ya", "WSnE"],
    projection="M15c",
    zsize="1.5c",
    # Sets the surface type to solid
    surftype="s",
)
fig.show()
