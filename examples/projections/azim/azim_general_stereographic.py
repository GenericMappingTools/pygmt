r"""
General Stereographic
=====================

This map projection is a conformal, azimuthal projection. It is mainly used with
a projection center in one of the poles. Then meridians appear as straight lines
and cross latitudes at a right angle. Unlike the azimuthal equidistant projection,
the distances in this projection are not displayed in correct proportions.
It is often used as a hemisphere map like the Lambert Azimuthal Equal Area
projection.

**s**\ *lon0/lat0*\ [*/horizon*]\ */scale*
or **S**\ *lon0/lat0*\ [*/horizon*\]\ */width*

The projection type is set with **s** or **S**. *lon0/lat0* specifies the
projection center, the optional *horizon* parameter specifies the max distance from
projection center (in degrees, < 180, default 90), and the *scale* or *width* sets the
size of the figure.
"""
import pygmt

fig = pygmt.Figure()
fig.coast(region="4/14/52/57", projection="S0/90/4.5i", frame="ag", land="gray")
fig.show()
