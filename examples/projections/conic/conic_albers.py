r"""
Albers Conic Equal Area
=======================

This projection, developed by Heinrich C. Albers in 1805, is predominantly used to map
regions of large east-west extent, in particular the United States. It is a conic,
equal-area projection, in which parallels are unequally spaced arcs of concentric
circles, more closely spaced at the north and south edges of the map. Meridians, on the
other hand, are equally spaced radii about a common center, and cut the parallels at
right angles. Distortion in scale and shape vanishes along the two standard parallels.
Between them, the scale along parallels is too small; beyond them it is too large.
The opposite is true for the scale along meridians.

**b**\ *lon0/lat0*\ /\ *lat1/lat2*\ */scale*
or **B**\ *lon0/lat0*\ /\ *lat1/lat2*\ */width*

The projection is set with **b** or **B**. The projection center is set by *lon0/lat0*
and two standard parallels for the map are set with *lat1/lat2*. The figure size is set
with *scale* or *width*.
"""
import pygmt

fig = pygmt.Figure()
# Use the ISO country code for Brazil and add a padding of 2 degrees (+R2)
fig.coast(
    projection="B-55/-15/-25/0/8i", region="BR+R2", frame="afg", land="gray", borders=1
)
fig.show()
