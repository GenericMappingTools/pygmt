"""
2. Create a contour map
=======================

This tutorial page covers the basics of creating a figure of Earth relief,
using a remote dataset hosted by GMT, using the method
:meth:`pygmt.datasets.load_earth_relief`. It will use
:meth:`pygmt.Figure.grdimage`, :meth:`pygmt.Figure.grdcontour`,
:meth:`pygmt.Figure.colorbar`, and :meth:`pygmt.Figure.coast` methods for
plotting.
"""

# sphinx_gallery_thumbnail_number = 1
import pygmt

###############################################################################
# Loading the Earth relief dataset
# --------------------------------
#
# The first step is to import :meth:`pygmt.datasets.load_earth_relief`.
# The ``resolution`` parameter sets the resolution of the remote grid file,
# which will affect the resolution of the plot made later in the tutorial.
# The ``registration`` parameter determines the grid registration.
#
# This grid region covers the islands of Guam and Rota in western Pacific
# Ocean.

grid = pygmt.datasets.load_earth_relief(
    resolution="30s", region=[144.5, 145.5, 13, 14.5], registration="gridline"
)

###############################################################################
# Plotting Earth relief
# ---------------------
#
# To plot Earth relief data, the method :meth:`pygmt.Figure.grdimage` can be
# used to plot a color-coded figure to display the topography and bathymetry
# in the grid file. The ``grid`` parameter accepts the input grid, which in
# this case is the remote file downloaded in the previous section. If the
# ``region`` parameter is not set, the region boundaries of the input grid are
# used.
#
# The ``cmap`` parameter sets the color palette table (CPT) used for
# portraying Earth relief. The :meth:`pygmt.Figure.grdimage` method used the
# input grid to apply Earth relief values to a specific color within the CPT.
# In this case, the CPT used is "haxby"; a full list of CPTs can be found
# at :gmt-docs:`cookbook/cpts.html`.

fig = pygmt.Figure()
fig.grdimage(grid=grid, frame="a", projection="M10c", cmap="haxby")
fig.show()

###############################################################################
# Adding a colorbar
# -----------------
#
# To show how the plotted colors relate to the Earth relief, a colorbar can be
# added using the :meth:`pygmt.Figure.colorbar` method.
#
# To control the labels on the colorbar, a list is passed to the ``frame``
# parameter. The value beginning with "a" sets the interval for annotation on
# the colorbar, in this case every 1,000 meters. To set the label for an axis
# on the colorbar, the value begins with either "x+l" (x-axis) or "y+l"
# (y-axis), followed by the intended label.
#
# By default, the CPT for the colorbar is the same as the one set
# in :meth:`pygmt.Figure.grdimage`.

fig = pygmt.Figure()
fig.grdimage(grid=grid, frame="a", projection="M10c", cmap="haxby")
fig.colorbar(frame=["a1000", "x+lElevation", "y+lm"])
fig.show()

###############################################################################
# Adding contour lines
# --------------------
#
# To add contour lines to the color coded figured, the
# :meth:`pygmt.Figure.grdcontour` method is used. The ``frame`` and
# ``projection`` are already set using :meth:`pygmt.Figure.grdimage` and are
# not needed again. However, the same input for ``grid`` (in this case, the
# variable named "grid") must be input again. The ``interval`` parameter sets
# the spacing between lines (in this case, 500 meters), and the ``annotation``
# parameter sets the spacing between darker lines that have the value on
# written on them (in this case, every 1,000 meters).

fig = pygmt.Figure()
fig.grdimage(grid=grid, frame="a", projection="M10c", cmap="haxby")
fig.grdcontour(grid=grid, interval=500, annotation=1000)
fig.colorbar(frame=["a1000", "x+lElevation (m)"])
fig.show()

###############################################################################
# Color in land
# -------------

###############################################################################
# Additional exercises
# --------------------
