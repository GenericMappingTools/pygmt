"""
Mollweide
=========

This pseudo-cylindrical, equal-area projection was developed by the German
mathematician and astronomer Karl Brandan Mollweide in 1805. Parallels are unequally
spaced straight lines with the meridians being equally spaced elliptical arcs. The
scale is only true along latitudes 40°44’ north and south. The projection is used
mainly for global maps showing data distributions. It is occasionally referenced under
the name homalographic projection.

``W[central meridian]/width``: Give the optional central meridian (default is the center
of the region) and the map width.
"""
import pygmt

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(region="d", projection="W12c", land="tomato1", water="skyblue", frame="ag")
fig.show()
