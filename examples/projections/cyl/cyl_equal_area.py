"""
Cylindrical equal-area
======================

This cylindrical projection is actually several projections, depending on what
latitude is selected as the standard parallel. However, they are all equal area and
hence non-conformal. All meridians and parallels are straight lines.

``Ylon0/lat0/width``: Give central meridian ``lon0``, the standard parallel ``lat0``,
and the figure ``width``.
"""
import pygmt

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(
    region="d",
    projection="Y35/30/12c",
    water="dodgerblue",
    shorelines="thinnest",
    frame="afg",
)
fig.show()
