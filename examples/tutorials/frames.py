"""
Frames, ticks, titles, and labels
=================================

Setting the style of the map frames, ticks, etc, is handled by the ``frame`` argument
that all plotting methods of :class:`pygmt.Figure`.
"""

import pygmt

########################################################################################
# Plot frame
# ----------
#
# By default, PyGMT does not add a frame to your plot. For example, we can plot the
# coastlines of the world with a Mercator projection:

fig = pygmt.Figure()
fig.coast(shorelines="1/0.5p", region=[-180, 180, -60, 60], projection="M25c")
fig.show()

########################################################################################
# To add the default GMT frame to the plot, use ``frame="f"`` in
# :meth:`pygmt.Figure.basemap` or any other plotting module:

fig = pygmt.Figure()
fig.coast(shorelines="1/0.5p", region=[-180, 180, -60, 60], projection="M25c")
fig.basemap(frame="f")
fig.show()

########################################################################################
# Ticks and grid lines
# --------------------
#
# The automatic frame (``frame=True`` or ``frame="a"``) sets the default GMT style frame
# and automatically determines tick labels from the plot region.

fig = pygmt.Figure()
fig.coast(shorelines="1/0.5p", region=[-180, 180, -60, 60], projection="M25c")
fig.basemap(frame="a")
fig.show()

########################################################################################
# Add automatic grid lines to the plot by adding a ``g`` to ``frame``:

fig = pygmt.Figure()
fig.coast(shorelines="1/0.5p", region=[-180, 180, -60, 60], projection="M25c")
fig.basemap(frame="ag")
fig.show()

########################################################################################
# Title
# -----
#
# The figure title can be set by passing ``"+t<title>"`` to the ``frame`` parameter of
# :meth:`pygmt.Figure.basemap`. Passing multiple arguments to ``frame`` can be done by
# using a list, as show in the example below.

fig = pygmt.Figure()
fig.coast(shorelines="1/0.5p", region="IS", projection="M25c")
fig.basemap(frame=["a", "+tIceland"])
fig.show()

########################################################################################
# To use a title with multiple words, the title must be placed inside another set of
# quotation marks. To prevent the quotation marks from appearing in the figure title,
# the frame argument can be passed in single quotation marks and the title can be
# passed in double quotation marks.

fig = pygmt.Figure()
fig.coast(shorelines="1/0.5p", region="TT", projection="M25c")
fig.basemap(frame=["a", '+t"Trinidad and Tobago"'])
fig.show()
