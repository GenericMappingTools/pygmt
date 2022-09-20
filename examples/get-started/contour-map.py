"""
2. Create a contour map
=======================

This tutorial page covers the basics of creating a figure of Earth relief,
using a remote dataset hosted by GMT, using the method
:meth:`pygmt.datasets.load_earth_relief`. It will use
:meth:`pygmt.Figure.grdimage`, :meth:`pygmt.Figure.grdcontour`,
and :meth:`pygmt.Figure.coast` methods for plotting.
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

###############################################################################
# Adding contour lines
# --------------------

###############################################################################
# Color in land
# -------------

###############################################################################
# Additional exercises
# --------------------
