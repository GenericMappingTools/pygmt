"""
Frames, ticks, titles, and labels
=================================

Setting frame, ticks, title, etc., of the plot is handled by the ``frame``
parameter that most plotting methods of the :class:`pygmt.Figure` class
contain.
"""
# sphinx_gallery_thumbnail_number = 4

import pygmt

###############################################################################
# Plot frame
# ----------
#
# By default, PyGMT does not add a frame to your plot. For example, we can plot
# the coastlines of the world with a Mercator projection:

fig = pygmt.Figure()
fig.coast(shorelines="1/0.5p", region=[-180, 180, -60, 60], projection="M25c")
fig.show()

###############################################################################
# To add the default GMT frame style to the plot, use ``frame="f"`` in
# :meth:`pygmt.Figure.basemap` or another plotting method (which has the
# ``frame`` parameter, with exception of :meth:`pygmt.Figure.colorbar`):

fig = pygmt.Figure()
fig.coast(shorelines="1/0.5p", region=[-180, 180, -60, 60], projection="M25c")
fig.basemap(frame="f")
fig.show()

###############################################################################
# Ticks and grid lines
# --------------------
#
# The automatic frame (``frame=True`` or ``frame="af"``) adds the default GMT
# frame style and automatically determines tick labels from the plot region.
# In GMT the tick labels are called **a**\ nnotations.

fig = pygmt.Figure()
fig.coast(shorelines="1/0.5p", region=[-180, 180, -60, 60], projection="M25c")
fig.basemap(frame="af")
fig.show()

###############################################################################
# Add automatic grid lines to the plot by passing ``g`` to ``frame``:

fig = pygmt.Figure()
fig.coast(shorelines="1/0.5p", region=[-180, 180, -60, 60], projection="M25c")
fig.basemap(frame="ag")
fig.show()

###############################################################################
# Title
# -----
#
# The figure title can be set by passing **+t**\ *title* to the ``frame``
# parameter of :meth:`pygmt.Figure.basemap`. Passing multiple arguments to
# ``frame`` can be done by using a list, as show in the example below.

fig = pygmt.Figure()
# region="IS" specifies Iceland using the ISO country code
fig.coast(shorelines="1/0.5p", region="IS", projection="M25c")
fig.basemap(frame=["a", "+tIceland"])
fig.show()

###############################################################################
# To use a title with multiple words, the title must be placed inside another
# set of quotation marks. To prevent the quotation marks from appearing in the
# figure title, the ``frame`` parameter can be passed in single quotation marks
# and the title can be passed in double quotation marks.

fig = pygmt.Figure()
# region="TT" specifies Trinidad and Tobago
fig.coast(shorelines="1/0.5p", region="TT", projection="M25c")
fig.basemap(frame=["a", '+t"Trinidad and Tobago"'])
fig.show()

###############################################################################
# Axis labels
# -----------
#
# Axis labels, in GMT simply called labels, can be set by passing
# **x+l**\ *label* (or starting with **y** if
# labeling the y-axis) to the ``frame`` parameter of
# :meth:`pygmt.Figure.basemap`. The map boundaries (or plot axes) are named as
# **W** (west/left), **S** (south/bottom), **N** (north/top), and
# **E** (east/right) sides of a figure. If an upper-case axis name is passed,
# the axis is plotted with tick marks and annotations. A lower-case axis name
# plots only the axis with tick marks. By default (``frame=True`` or
# ``frame="af"``), the west/left and the south/bottom axes are plotted with
# both tick marks and annotations.
#
# The example below uses a Cartesian projection, as GMT does not allow
# labels to be set for geographic maps.

fig = pygmt.Figure()
fig.basemap(
    region=[0, 10, 0, 20],
    projection="X10c/8c",
    # Plot axis with tick marks, annotations, and labels on the
    # west/left and south/bottom axes
    # Plot axis with tick marks on the north/top and east/right axes
    frame=["WSne", "xaf+lx-axis", "yaf+ly-axis"],
)
fig.show()
