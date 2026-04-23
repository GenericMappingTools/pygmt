"""
Frames, ticks, titles, and labels
=================================

Setting frame, ticks, titles, and labels is handled by the ``frame`` parameter that
many plotting methods of the :class:`pygmt.Figure` class accept. This tutorial focuses
on the higher-level :class:`pygmt.params.Axis` and :class:`pygmt.params.Frame`
classes.
"""

# %%
import pygmt
from pygmt.params import Axis, Frame

# %%
# Plot frame
# ----------
#
# By default, PyGMT does not add a frame to your plot. For example, we can plot the
# coastlines of the world with a Mercator projection:

fig = pygmt.Figure()
fig.coast(shorelines="1/0.5p", region=[-180, 180, -60, 60], projection="M25c")
fig.show()

# %%
# To add the default GMT frame style to the plot, use ``frame=True`` in
# :meth:`pygmt.Figure.basemap` or another plotting method that accepts a ``frame``
# parameter:

fig = pygmt.Figure()
fig.coast(shorelines="1/0.5p", region=[-180, 180, -60, 60], projection="M25c")
fig.basemap(frame=True)
fig.show()


# %%
# Tick marks and grid lines
# -------------------------
#
# For more control, use :class:`pygmt.params.Axis` to describe annotations, tick marks,
# and gridlines. In GMT, tick labels are called **a**\ nnotations.

fig = pygmt.Figure()
fig.coast(shorelines="1/0.5p", region=[-180, 180, -60, 60], projection="M25c")
fig.basemap(frame=Axis(annot=True))
fig.show()

# %%
# Here, ``annot=True`` asks GMT to choose annotation intervals automatically, and
# ``grid=True`` adds automatic grid lines:

fig = pygmt.Figure()
fig.coast(shorelines="1/0.5p", region=[-180, 180, -60, 60], projection="M25c")
fig.basemap(frame=Axis(annot=True, grid=True))
fig.show()

# %%
# To set specific intervals, pass values to ``annot``, ``tick``, and ``grid``. In the
# example below, the annotation, tick, and gridline intervals are set to 30, 7.5, and
# 15 degrees, respectively.

fig = pygmt.Figure()
fig.coast(shorelines="1/0.5p", region=[-180, 180, -60, 60], projection="M25c")
fig.basemap(frame=Axis(annot=30, tick=7.5, grid=15))
fig.show()

# %%
# Title
# -----
#
# The :class:`pygmt.params.Frame` class lets us configure frame-wide settings such as
# titles. Combine it with an :class:`Axis` object to keep automatic annotations.

fig = pygmt.Figure()
# region="TT" specifies Trinidad and Tobago using the ISO country code
fig.coast(shorelines="1/0.5p", region="TT", projection="M25c")
fig.basemap(frame=Frame(title="Trinidad and Tobago", axis=Axis(annot=True)))
fig.show()


# %%
# Axis labels
# -----------
#
# Axis labels, in GMT simply called labels, can be set through the ``xaxis`` and
# ``yaxis`` parameters of :class:`Frame`. The map boundaries (or plot axes) are named
# as West/west/left (**W**, **w**, **l**), South/south/bottom (**S**, **s**, **b**),
# North/north/top (**N**, **n**, **t**), and East/east/right (**E**, **e**, **r**)
# sides of a figure. Uppercase letters (**W**, **S**, **N**, **E**) draw axes with
# annotations and tick marks, lowercase letters (**w**, **s**, **n**, **e**) draw
# axes with tick marks only, and **l**, **b**, **t**, **r** draw plain axis lines
# without ticks or annotations. A frame like ``Frame(axes="WS")`` draws annotated west
# and south axes only.
#
# The example below uses a Cartesian projection, as GMT does not allow
# labels to be set for geographic maps.

fig = pygmt.Figure()
fig.basemap(
    region=[0, 10, 0, 20],
    projection="X10c/8c",
    # Plot axis with tick marks, annotations, and labels on the
    # West and South axes
    # Plot axis with tick marks on the north and east axes
    frame=Frame(
        axes="WSne",
        xaxis=Axis(annot=True, tick=True, label="x-axis"),
        yaxis=Axis(annot=True, tick=True, label="y-axis"),
    ),
)
fig.show()

# sphinx_gallery_thumbnail_number = 4
