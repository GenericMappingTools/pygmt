"""
Hammer
======

The equal-area Hammer projection, first presented by the German mathematician
Ernst von Hammer in 1892, is also known as Hammer-Aitoff (the Aitoff projection looks
similar, but is not equal-area). The border is an ellipse, equator and central
meridian are straight lines, while other parallels and meridians are complex curves.

**h**\ [*lon0/*]\ *scale* or **H**\ [*lon0/*]\ *width*

The projection is set with **h** or **H**. The central meridian is set with the
optional *lon0*, and the figure size is set with *scale* or *width*.
"""
import pygmt

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(region="d", projection="H12c", land="black", water="cornsilk", frame="afg")
fig.show()
