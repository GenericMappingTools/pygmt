"""
Creating a map with contour lines
=================================

Plotting a contour map is handled by :meth:`pygmt.Figure.grdcontour`
"""

import pygmt

########################################################################################
# Create contour plot
# -------------------
#
# The grdcontour method takes the grid input and the region values.
# It plots annotated contour lines, which are darker and have the elevation/depth written on them,
# and unannotated contour lines. In the example blow, the default contour line intervals are 500 meters,
# with an annotated contour line every 1000 meters.
# By default, it plots the map with a Equidistant cylindrical projection and with no frame.

fig = pygmt.Figure()
fig.grdcontour(grid="@earth_relief_15s", region=[-92, -90, -1.5, 0.5])
fig.show()

########################################################################################
# Contour line settings
# ---------------------
#
# Use the "annotation" and "interval" arguments to adjust contour line intervals
# In the example below, there are contour intervals every 250 meters and an annotated contour line every 1,000 meters.

fig = pygmt.Figure()
fig.grdcontour(
    annotation=1000,
    interval=250,
    grid="@earth_relief_15s",
    region=[-92, -90, -1.5, 0.5],
)
fig.show()

########################################################################################
# Contour limits
# --------------
#
# The limit argument sets the minimum and maximum values for the contour lines, with the value.
# The argument takes the low and high values, and is either a list (as below) or a string  limit="-4000/0"

fig = pygmt.Figure()
fig.grdcontour(
    annotation=1000,
    interval=250,
    grid="@earth_relief_15s",
    region=[-92, -90, -1.5, 0.5],
    limit=[-4000, 0],
)
fig.show()

########################################################################################
# Map settings
# ------------
#
# The grdcontour method accepts additional arguments, including setting the projection and frame.

fig = pygmt.Figure()
fig.grdcontour(
    annotation=1000,
    interval=250,
    grid="@earth_relief_15s",
    region=[-92, -90, -1.5, 0.5],
    limit=[-4000, 0],
    projection="M4i",
    frame=True,
)
fig.show()
