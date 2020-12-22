"""
Equidistant conic
=================

The equidistant conic projection was described by the Greek philosopher Claudius
Ptolemy about A.D. 150. It is neither conformal or equal-area, but serves as a
compromise between them. The scale is true along all meridians and the
standard parallels.

``Dlon0/lat0/lat1/lat2/width``: Give projection center ``lon0/lat0``, two standard
parallels ``lat1/lat2``, and the map width.
"""
import pygmt

fig = pygmt.Figure()
fig.coast(
    shorelines="1/0.5p",
    region=[-88, -70, 18, 24],
    projection="D-79/21/19/23/12c",
    land="lightgreen",
    water="lightblue",
    frame="afg",
)

fig.show()
