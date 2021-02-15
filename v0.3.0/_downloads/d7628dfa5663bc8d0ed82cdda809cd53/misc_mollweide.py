"""
Mollweide
=========

This pseudo-cylindrical, equal-area projection was developed by the German
mathematician and astronomer Karl Brandan Mollweide in 1805. Parallels are unequally
spaced straight lines with the meridians being equally spaced elliptical arcs. The
scale is only true along latitudes 40°44’ north and south. The projection is used
mainly for global maps showing data distributions. It is occasionally referenced under
the name homalographic projection.

**w**\ [*lon0/*]\ *scale* or **W**\ [*lon0/*]\ *width*

The projection is set with **w** or **W**. The central meridian is set with the
optional *lon0*, and the figure size is set with *scale* or *width*.
"""
import pygmt

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(region="d", projection="W12c", land="tomato1", water="skyblue", frame="ag")
fig.show()
