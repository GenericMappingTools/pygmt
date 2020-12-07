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

# :meth:`pygmt.Figure.grdimage` can take the optional argument ``projection`` for the
# map. In the example below, the ``projection`` is set as "`R5i`" for 5-inch figure
# with a Winkel Tripel projection. For a list of available projections,
# see :gmt-docs:`cookbook/map_projections.html`.

fig = pygmt.Figure()
fig.grdimage(grid=grid, projection="R5i")
fig.show()

########################################################################################
# A specific color palette can be set using the optional ``cmap`` argument for
# :meth:`pygmt.Figure.grdimage`. By default, the color palette is set to *turbo*.
# In the example below, the color palette is set to *geo*.
# The full list of color palette tables can be found at :gmt-docs:`cookbook/cpts.html`.

fig = pygmt.Figure()
fig.grdimage(grid=grid, cmap="geo")
fig.show()

########################################################################################
# :meth:`pygmt.Figure.grdimage` accepts additional parameters, including  ``frame`` and
# ``projection``.

fig = pygmt.Figure()
fig.grdimage(grid=grid, frame=True, projection="M6i", cmap="geo")
fig.show()

########################################################################################
# The :meth:`pygmt.Figure.colorbar` method can be used to add a color bar to the figure.
# By default, it applies the color palette created by :meth:`pygmt.Figure.grdimage`.
#
# The `frame` argument can be used to set the color bar labels and intervals.
# In the example below, ``p3000`` sets the color bar tick interval to 3,000 meters,
# and ``x+lElevation`` and ``y+lm`` set the x- and y-axis labels for the color bar.

fig = pygmt.Figure()
fig.grdimage(grid=grid, frame=True, projection="M6i", cmap="geo")
fig.colorbar(frame=["p3000", "x+lElevation", "y+lm"])
fig.show()
