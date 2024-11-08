r"""
Plotting single-parameter symbols
=================================

The :meth:`pygmt.Figure.plot` method can plot symbols via the ``style``, ``size``, and
``symbol`` parameters. Via the ``fill`` parameter the symbols can be filled with a color
or pattern. The ``pen`` parameter can add an outline by providing a string argument in
the form *width*,\ *color*,\ *style*. The defaults are no fill and a 0.25-points thick,
black, solid outline. For the available patterns see the Technical Reference
:doc:`Bit and hachure patterns </techref/patterns>`. For details on adjusting ``pen``
see the Gallery example :doc:`Line styles </gallery/lines/linestyles>`. For the
available single- and multi-parameter symbols see the Gallery examples
:doc:`Single-parameter symbols </gallery/symbols/basic_symbols>` and
:doc:`Multi-parameter symbols </gallery/symbols/multi_parameter_symbols>`, respectively.
"""

# %%
import pygmt

# Set up five sample data points as lists for the x and y values
x = [-4, -2, 0, 2, 4]
y = [0] * len(x)


# %%
# Use the ``style`` parameter of the :meth:`pygmt.Figure.plot` method to plot all data
# points with the same symbol and size.

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -2, 2], projection="X10c/4c", frame=True)

# Plot circles (first "c") with a diameter of 0.5 centimeters (second "c")
fig.plot(x=x, y=y, style="c0.5c", fill="gray", pen="1p,orange")

fig.show()


# %%
# Use the ``size`` parameter to plot the data points with individual sizes. Provide
# the different sizes as a list or array of floats.

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -2, 2], projection="X10c/4c", frame=True)

fig.plot(
    x=x,
    y=y,
    # Plot circles (first "c") with a diameter in centimeters (second "c")
    style="cc",
    # Use individual sizes
    size=[0.5, 0.2, 0.4, 0.6, 0.3],
    fill="gray",
    pen="1p,orange",
)

fig.show()


# %%
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
    # Plot a circle, a square, a triangle, a inverse triangle, a diamond
    symbol=["c", "s", "t", "i", "d"],
    fill="gray",
    pen="1p,orange",
)

fig.show()


# %%
# Use the ``symbol`` and ``size`` parameters together to plot the data points with
# individual symbols and sizes. ``symbol`` and ``size`` need to have the same length.
# The unit used by ``size`` is now set via the GMT default parameter
# ``PROJ_LENGTH_UNIT`` and is by default centimeters. Use :class:`pygmt.config` to
# change this.

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -2, 2], projection="X10c/4c", frame=True)

fig.plot(
    x=x,
    y=y,
    symbol=["c", "s", "t", "i", "d"],
    size=[0.5, 0.2, 0.4, 0.6, 0.3],
    fill="gray",
    pen="1p,orange",
)

fig.show()

# sphinx_gallery_thumbnail_number = 4
