"""
Plotting Earth relief
=====================

Plotting a map of Earth relief can use the data accessed by the
:meth:`pygmt.datasets.load_earth_relief` method. The data can then be plotted using the
:meth:`pygmt.Figure.grdimage` method.
"""

import pygmt

# Load sample Earth relief data for the entire globe at a resolution of 30 minutes.
# The other available resolutions are show at :gmt-docs:`datasets/earth_relief.html`.
grid = pygmt.datasets.load_earth_relief(resolution="30m")

########################################################################################
# Create a plot
# -------------
#
# The :meth:`pygmt.Figure.grdimage` method takes the ``grid`` input a
# create a figure. It creates and applies a color palette to the figure based upon the
# z-values of the data. By default, it plots the map with the the *turbo* CPT, an
# equidistant cylindrical projection, and with no frame.

fig = pygmt.Figure()
fig.grdimage(grid=grid)
fig.show()

########################################################################################
#
# :meth:`pygmt.Figure.grdimage` can take the optional argument ``projection`` for the
# map. In the example below, the ``projection`` is set as ``"R5i"`` for 5-inch figure
# with a Winkel Tripel projection. For a list of available projections,
# see :gmt-docs:`cookbook/map_projections.html`.

fig = pygmt.Figure()
fig.grdimage(grid=grid, projection="R5i")
fig.show()

########################################################################################
# Set a color map
# ---------------
#
# :meth:`pygmt.Figure.grdimage` takes the ``cmap`` argument to set the CPT of the
# figure. Examples of common CPTs for Earth relief are shown below.
# A full list of CPTs can be found at :gmt-docs:`cookbook/cpts.html`.

########################################################################################
#
# *geo*

fig = pygmt.Figure()
fig.grdimage(grid=grid, projection="R5i", cmap="geo")
fig.show()

########################################################################################
#
# *relief*

fig = pygmt.Figure()
fig.grdimage(grid=grid, projection="R5i", cmap="relief")
fig.show()

########################################################################################
#
# *etopo1*

fig = pygmt.Figure()
fig.grdimage(grid=grid, projection="R5i", cmap="etopo1")
fig.show()

########################################################################################
# Add a color bar
# ---------------
#
# The :meth:`pygmt.Figure.colorbar` method displays the CPT and the associated Z-values
# of the figure, and by default uses the same CPT set by the ``cmap`` argument
# for :meth:`pygmt.Figure.grdimage`. The ``frame`` argument for
# :meth:`pygmt.Figure.colorbar` can be used to set the axis intervals and labels. A
# list is used to pass multiple arguments to ``frame``. In the example below,
# ``"p2500"`` sets the axis interval to 2,500, ``"x+lElevation"`` sets  the x-axis
# label, and ``"y+lm"`` sets the y-axis label.

fig = pygmt.Figure()
fig.grdimage(grid=grid, projection="R5i", cmap="geo")
fig.colorbar(frame=["p2500", "x+lElevation", "y+lm"])
fig.show()

########################################################################################
# Create a region map
# -------------------
#
# In addition to providing global data, the ``region`` argument for
# ``pygmt.datasets.load_earth_relief`` can be used to provide data for a specific
# area. The ``region`` argument is required for resolutions at 5 minutes or lower, and
# accepts a list (as in the example below) or a string. The geographic ranges are
# passed as *x-min*/*x-max*/*y-min*/*y-max*.
#
# The example below uses data with a 5 minute resolution, and plots it on a 6 inch
# figure with a Mercator projection and a CPT set to *geo*.
# :meth:`pygmt.Figure.basemap` is used to add a frame to the figure, using the argument
# ``"a"`` for the ``frame`` parameter.

grid = pygmt.datasets.load_earth_relief(resolution="05m", region=[-14, 30, 35, 60])
fig = pygmt.Figure()
fig.grdimage(grid=grid, projection="M6i", cmap="geo")
fig.basemap(frame="a")
fig.colorbar(frame=["p1000", "x+lElevation", "y+lm"])
fig.show()
