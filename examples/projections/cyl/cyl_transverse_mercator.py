"""
Transverse Mercator
===================

``T[lon0/][lat0/]width``: Give central meridian ``lon0``, the latitude of the
origin ``lat0`` (optional), and the figure width.
"""
import pygmt

fig = pygmt.Figure()
fig.coast(
    region=[20, 50, 30, 45],
    projection="T35/12c",
    land="lightbrown",
    water="seashell",
    shorelines="thinnest",
    frame="afg",
)
fig.show()
