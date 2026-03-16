"""
Plotting single-parameter symbols
=================================

The :meth:`pygmt.Figure.plot` method can plot symbols via the ``style``, ``size``, and
``symbol`` parameters. This tutorial focuses on single-parameter symbols; for an
overview of the available single-parameter symbols, see the Gallery example
:doc:`Single-parameter symbols </gallery/symbols/basic_symbols>`. The available multi-
parameter symbols are explained in the Gallery example
:doc:`Multi-parameter symbols </gallery/symbols/multi_parameter_symbols>`.
"""

# %%
import numpy as np
import pygmt

# Set up five sample data points as NumPy arrays for the x and y values
x = np.array([-4, -2, 0, 2, 4])
y = np.array([0, 0, 0, 0, 0])


# %%
# Plot single-parameter symbols
# -----------------------------
#
# Use the ``style`` parameter of the :meth:`pygmt.Figure.plot` method to plot all data
# points with the same symbol and size. By default, the symbol is drawn unfilled with
# an 0.25-points, thick, solid outline. Use the ``pen`` parameter to adjust the outline
# by providing a string argument in the form *width*,\ *color*,\ *style*; for details
# see the Gallery example :doc:`Line styles </gallery/lines/linestyles>`.

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -2, 2], projection="X10c/4c", frame=True)

# Plot circles (first "c") with a diameter of 0.5 centimeters (second "c")
fig.plot(x=x, y=y, style="c0.5c")

fig.shift_origin(xshift="w+1c")
fig.basemap(region=[-5, 5, -2, 2], projection="X10c/4c", frame=True)

# Adjust the outline via the pen parameter
fig.plot(x=x, y=y, style="c0.5c", pen="1p,orange")

fig.show()

# %%
# Use the ``fill`` the parameter to add a fill color or pattern. Note, that no outline
# is drawn by default when ``fill`` is used. For the available patterns see the
# Technical Reference :doc:`Bit and hachure patterns </techref/patterns>`.

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -2, 2], projection="X10c/4c", frame=True)

# Add a color via the fill parameter
fig.plot(x=x, y=y, style="c0.5c", fill="gray")

fig.shift_origin(xshift="w+1c")
fig.basemap(region=[-5, 5, -2, 2], projection="X10c/4c", frame=True)

# Add an outline via the pen parameter
fig.plot(x=x, y=y, style="c0.5c", fill="gray", pen="1p,orange")

fig.show()


# %%
# Use individual sizes
# --------------------
#
# Use the ``size`` parameter to plot the data points with individual sizes. Provide
# the different sizes as a NumPy array or array-like object of integers or floats.

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -2, 2], projection="X10c/4c", frame=True)

fig.plot(
    x=x,
    y=y,
    # Plot circles (first "c") with a diameter in centimeters (second "c")
    style="cc",
    # Use individual sizes
    size=np.array([0.5, 0.2, 0.4, 0.6, 0.3]),
    fill="gray",
    pen="1p,orange",
)

fig.show()


# %%
# Use individual symbols
# ----------------------
#
# Use the ``symbol`` parameter to plot the data points with individual symbols. Provide
# the different symbols as a list of strings. Here, only single-parameter symbols can
# be used.

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -2, 2], projection="X10c/4c", frame=True)

fig.plot(
    x=x,
    y=y,
    # Use a constant size of 0.5 centimeters
    style="0.5c",
    # Plot a circle, a square, a triangle, an inverse triangle, a diamond
    symbol=["c", "s", "t", "i", "d"],
    fill="gray",
    pen="1p,orange",
)

fig.show()


# %%
# Use individual symbols and sizes
# --------------------------------
#
# Use the ``symbol`` and ``size`` parameters together to plot the data points with
# individual symbols and sizes. The arguments passed to ``symbol`` and ``size`` must
# have the same length. The unit for ``size`` is now set via the GMT default parameter
# ``PROJ_LENGTH_UNIT`` which can by adjusted using :class:`pygmt.config` [Default is
# centimeters].

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -2, 2], projection="X10c/4c", frame=True)

fig.plot(
    x=x,
    y=y,
    symbol=["c", "s", "t", "i", "d"],
    size=np.array([0.5, 0.2, 0.4, 0.6, 0.3]),
    fill="gray",
    pen="1p,orange",
)

fig.show()

# sphinx_gallery_thumbnail_number = 5
