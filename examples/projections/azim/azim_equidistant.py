r"""
Azimuthal Equidistant
=====================

The main advantage of this projection is that distances from the projection
center are displayed in correct proportions. Also directions measured from the
projection center are correct. It is very useful for a global view on locations
that lie within a certain distance or for comparing distances of different
locations relative to the projection center.

**e**\ *lon0/lat0*\ [*/horizon*]\ */scale* or
**E**\ *lon0/lat0*\ [*/horizon*]\ */width*

The projection type is set with **e** or **E**, *lon0/lat0* specifies the projection
center, and the optional parameter *horizon* specifies the max distance to the
projection center (i.e. the visibile portion of the rest of the world map) in
degrees <= 180° (default 180°). The size of the figure is set by *scale* or *width*.
"""
import pygmt

fig = pygmt.Figure()
fig.coast(projection="E-100/40/4.5i", region="g", frame="g", land="gray")
fig.show()
