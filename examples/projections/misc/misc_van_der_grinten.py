"""
Van der Grinten
===============

The Van der Grinten projection, presented by Alphons J. van der Grinten in 1904, is
neither equal-area nor conformal. Central meridian and Equator are straight lines;
other meridians are arcs of circles. The scale is true along the Equator only. Its
main use is to show the entire world enclosed in a circle.

``V[central meridian]/width``: Give the optional central meridian (default is the center
of the region) and the map width.
"""
import pygmt

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(region="d", projection="V12c", land="gray", water="cornsilk", frame="afg")
fig.show()
