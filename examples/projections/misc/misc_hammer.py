"""
Hammer
======

``H[central meridian]/width``: Give the optional central meridian (default is the center
 of the region) and the map width.
"""
import pygmt

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(region="d", projection="H12c", land="black", water="cornsilk", frame="afg")
fig.show()
