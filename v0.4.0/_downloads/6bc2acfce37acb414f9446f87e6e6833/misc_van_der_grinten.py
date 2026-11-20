"""
Van der Grinten
===============

The Van der Grinten projection, presented by Alphons J. van der Grinten in 1904, is
neither equal-area nor conformal. Central meridian and Equator are straight lines;
other meridians are arcs of circles. The scale is true along the Equator only. Its
main use is to show the entire world enclosed in a circle.

**v**\ [*lon0/*]\ *scale* or **V**\ [*lon0/*]\ *width*

The projection is set with **v** or **V**. The central meridian is set with the
optional *lon0*, and the figure size is set with *scale* or *width*.
"""
import pygmt

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(region="d", projection="V12c", land="gray", water="cornsilk", frame="afg")
fig.show()
