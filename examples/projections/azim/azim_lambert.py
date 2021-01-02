r"""
Lambert Azimuthal Equal Area
============================

This projection was developed by Johann Heinrich Lambert in 1772 and is typically used
for mapping large regions like continents and hemispheres. It is an azimuthal,
equal-area projection, but is not perspective. Distortion is zero at the center of the
projection, and increases radially away from this point.

**a**\ *lon0/lat0*\ [*/horizon*\ ]\ */scale*
or **A**\ *lon0/lat0*\ [*/horizon*\ ]\ */width*

**a** or **A** specifies the projection type, and *lon0/lat0* specifies the projection
center, *horizon* specifies the max distance from projection center (in degrees,
<= 180, default 90), and *scale* or *width* sets the size of the figure.
"""
import pygmt

fig = pygmt.Figure()
fig.coast(region="g", frame="afg", land="gray", projection="A30/-20/60/8i")
fig.show()
