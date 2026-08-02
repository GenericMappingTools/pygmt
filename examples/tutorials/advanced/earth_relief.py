"""
Plotting Earth relief
=====================

PyGMT provides the :func:`pygmt.datasets.load_earth_relief` function to download the
Earth relief data from the GMT remote server and load as an :class:`xarray.DataArray`
object. The data can then be plotted using the :meth:`pygmt.Figure.grdimage` method.
"""

# %%
import pygmt
from pygmt.params import Axis

# %%
# Load sample Earth relief data for the entire globe at a resolution of 1 arc-degree.
# Refer to :func:`pygmt.datasets.load_earth_relief` for the other available resolutions.
grid = pygmt.datasets.load_earth_relief(resolution="01d")


# %%
# Create a plot
# -------------
#
# The :meth:`pygmt.Figure.grdimage` method takes the ``grid`` input to create a figure.
# It creates and applies a color palette to the figure based upon the z-values of the
# data. By default, it plots the map with the *turbo* CPT, an equidistant cylindrical
# projection, and with no frame.

fig = pygmt.Figure()
fig.grdimage(grid=grid)
fig.show()

# %%
# :meth:`pygmt.Figure.grdimage` can take the optional parameter ``projection`` for the
# map. In the example below, ``projection`` is set to ``"R12c"`` for a
# 12-centimeters-wide figure with a Winkel Tripel projection. For a list of available
# projections, see :doc:`/techref/projections`.

fig = pygmt.Figure()
fig.grdimage(grid=grid, projection="R12c")
fig.show()


# %%
# Set a colormap
# --------------
#
# :meth:`pygmt.Figure.grdimage` takes the ``cmap`` parameter to set the CPT of the
# figure. Examples of common CPTs for Earth relief are shown below. A full list of CPTs
# can be found at :gmt-docs:`reference/cpts.html`.

# %%
# Using the *geo* CPT:

fig = pygmt.Figure()
fig.grdimage(grid=grid, projection="R12c", cmap="gmt/geo")
fig.show()

# %%
# Using the *relief* CPT:

fig = pygmt.Figure()
fig.grdimage(grid=grid, projection="R12c", cmap="gmt/relief")
fig.show()


# %%
# Add a colorbar
# --------------
#
# The :meth:`pygmt.Figure.colorbar` method displays the CPT and the associated z-values
# of the figure, and by default uses the same CPT set by the ``cmap`` parameter for
# :meth:`pygmt.Figure.grdimage`. The ``annot`` parameter sets the annotation interval,
# the ``label`` parameter sets the x-axis label, and the ``unit`` parameter sets the
# y-axis label.

fig = pygmt.Figure()
fig.grdimage(grid=grid, projection="R12c", cmap="gmt/geo")
fig.colorbar(annot=2500, label="Elevation", unit="m")
fig.show()


# %%
# Create a region map
# -------------------
#
# In addition to providing global data, the ``region`` parameter of
# :func:`pygmt.datasets.load_earth_relief` can be used to provide data for a specific
# area. The ``region`` parameter is required for resolutions at 5 arc-minutes or higher,
# and accepts a list in the form of [*xmin*, *xmax*, *ymin*, *ymax*].
#
# The example below uses data with a 10 arc-minutes resolution, and plots it on a
# 15-centimeters-wide figure with a Mercator projection and a CPT set to *geo*.
# ``frame=Axis(annot=True)`` is used to add a frame with annotations to the figure.

grid = pygmt.datasets.load_earth_relief(resolution="10m", region=[-14, 30, 35, 60])
fig = pygmt.Figure()
fig.grdimage(grid=grid, projection="M15c", frame=Axis(annot=True), cmap="gmt/geo")
fig.colorbar(annot=1000, label="Elevation", unit="m")
fig.show()

# sphinx_gallery_thumbnail_number = 5
