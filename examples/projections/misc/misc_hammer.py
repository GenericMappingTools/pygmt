"""
Hammer
======

The equal-area Hammer projection, first presented by the German mathematician
Ernst von Hammer in 1892, is also known as Hammer-Aitoff (the Aitoff projection looks
similar, but is not equal-area). The border is an ellipse, equator and central
meridian are straight lines, while other parallels and meridians are complex curves.

``H[central meridian]/width``: Give the optional central meridian (default is the center
of the region) and the map width.
"""
import pygmt

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(region="d", projection="H12c", land="black", water="cornsilk", frame="afg")
fig.show()
