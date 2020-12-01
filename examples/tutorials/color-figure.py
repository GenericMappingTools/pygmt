"""
Adding a color pallete to a figure
==================================

Plotting a map with a color pallete is handled by :meth:`pygmt.Figure.grdimage`. The
:meth:`pygmt.makecpt` method creates a custom color pallete that can be used with
the figures and color bars.
"""

import pygmt

# Load sample earth relief data
grid = pygmt.datasets.load_earth_relief(resolution="05m", region=[-86, -64, 17, 24])

########################################################################################
# Create a plot with color
# ------------------------
#
# The :meth:`pygmt.Figure.grdimage` method takes the ``grid`` input and optional
# ``region`` argument to create a figure. It creates and applies a color pallete to the
# figure based upon the z-values of the data. By default, it plots the map with the
# equidistant cylindrical projection and with no frame.

fig = pygmt.Figure()
fig.grdimage(grid=grid)
fig.show()

########################################################################################
# :meth:`pygmt.Figure.grdimage` accepts additional parameters, including  ``frame`` and
# ``projection``.

fig = pygmt.Figure()
fig.grdimage(grid=grid, frame=True, projection="M4i")
fig.show()

########################################################################################
# The :meth:`pygmt.Figure.colorbar` method can be used to add a color bar to the figure.
# By default, it applies the color pallete created by :meth:`pygmt.Figure.grdimage`.

fig = pygmt.Figure()
fig.grdimage(grid=grid, frame=True, projection="M4i")
fig.colorbar(frame=["x+lElevation", "y+lm"])
fig.show()