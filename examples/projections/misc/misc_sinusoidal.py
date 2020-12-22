"""
Sinusoidal
==========

The sinusoidal projection is one of the oldest known projections, is equal-area, and
has been used since the mid-16th century. It has also been called the
“Equal-area Mercator” projection. The central meridian is a straight line; all other
meridians are sinusoidal curves. Parallels are all equally spaced straight lines, with
scale being true along all parallels (and central meridian).

``I[central meridian]/width``: Give the optional central meridian (default is the center
 of the region) and the map width.
"""
import pygmt

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(region="d", projection="I12c", land="coral4", water="azure3", frame="afg")
fig.show()
