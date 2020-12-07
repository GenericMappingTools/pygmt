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
# map. In the example below, the ``projection`` is set as "`R5i`" for 5-inch figure
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
