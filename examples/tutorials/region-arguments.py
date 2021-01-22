"""
Set the region argument
=======================

Many of the plotting functions take an argument for the ``region`` argument, which sets
the area that will be shown in the figure. This tutorial covers the different types of
inputs that it can accept.
"""

import pygmt

########################################################################################
# Coordinates
# -----------
#
# A string of coordinates can be passed to ``region``, in the form of
# *xmin*\ /*xmax*\ /*ymin*\ /*ymax*\ .

fig = pygmt.Figure()
fig.coast(
    # Sets the x-range from 10E to 20E and the y-range to 35N to 45N
    region="10/20/35/45",
    # Set projection to Mercator, and the figure size to 15 centimeters
    projection="M15c",
    # Set the color of the land to light gray
    land="lightgray",
    # Set the color of the water to white
    water="white",
    # Display the national borders and set the pen-size to 0.5p
    borders="1/0.5p",
    # Display the shorelines and set the pen-size to 0.5p
    shorelines="1/0.5p",
    # Set the frame to automatic and display gridlines
    frame="ag",
)
fig.show()

########################################################################################
#
# The coordinates coordinates can be passed to ``region`` as a list, in the form of
#  [\ *xmin*\ ,*xmax*\ ,*ymin*\ ,*ymax*\ ].

fig = pygmt.Figure()
fig.coast(
    # Sets the x-range from 10E to 20E and the y-range to 35N to 45N
    region=[10, 20, 35, 45],
    projection="M12c",
    land="lightgray",
    water="white",
    borders="1/0.5p",
    shorelines="1/0.5p",
    frame="ag",
)
fig.show()

########################################################################################
#
# GMT has the option for region coordinates to be passed in classic mode, which was the
# standard prior to GMT version 6. The string format takes the coordinates for the
# bottom-left and top-right coordinates. To specify classic mode, append **+r** at the
# end of the ``region`` string.

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(
    region="10/35/20/45+r",
    projection="M12c",
    land="lightgray",
    water="white",
    borders="1/0.5p",
    shorelines="1/0.5p",
    frame="ag",
)
fig.show()

########################################################################################
#
# Passing **g** to ``region`` sets the region to

fig = pygmt.Figure()
fig.coast(
    region="g", projection="Cyl_stere/12c", land="tomato1", water="skyblue", frame="ag"
)
fig.show()

########################################################################################
# Contour line settings
# ---------------------
#
# Use the ``annotation`` and ``interval`` arguments to adjust contour line intervals.
# In the example below, there are contour intervals every 250 meters and
# annotated contour lines every 1,000 meters.

fig = pygmt.Figure()
fig.grdcontour(
    annotation=1000,
    interval=250,
    grid=grid,
)
fig.show()

########################################################################################
# Contour limits
# --------------
#
# The ``limit`` argument sets the minimum and maximum values for the contour lines.
# The argument takes the low and high values,
# and is either a list (as below) or a string ``limit="-4000/-2000"``.

fig = pygmt.Figure()
fig.grdcontour(
    annotation=1000,
    interval=250,
    grid=grid,
    limit=[-4000, -2000],
)
fig.show()

########################################################################################
# Map settings
# ------------
#
# The :meth:`pygmt.Figure.grdcontour` method accepts additional arguments,
# including setting the projection and frame.

fig = pygmt.Figure()
fig.grdcontour(
    annotation=1000,
    interval=250,
    grid=grid,
    limit=[-4000, -2000],
    projection="M10c",
    frame=True,
)
fig.show()

########################################################################################
# Adding a colormap
# -----------------
#
# The :meth:`pygmt.Figure.grdimage` method can be used to add a
# colormap to the contour map. It must be called prior to
# :meth:`pygmt.Figure.grdcontour` to keep the contour lines visible on the final map.
# If the ``projection`` argument is specified in the :meth:`pygmt.Figure.grdimage`
# method, it does not need to be repeated in the :meth:`pygmt.Figure.grdcontour` method.

fig = pygmt.Figure()
fig.grdimage(
    grid=grid,
    cmap="haxby",
    projection="M10c",
    frame=True,
)
fig.grdcontour(
    annotation=1000,
    interval=250,
    grid=grid,
    limit=[-4000, -2000],
)
fig.show()
