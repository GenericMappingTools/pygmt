"""
Cylindrical equal-area
======================

``Ylon0/lat0/width``: Give central meridian ``lon0``, the standard parallel ``lat0``, and the figure ``width``.
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
