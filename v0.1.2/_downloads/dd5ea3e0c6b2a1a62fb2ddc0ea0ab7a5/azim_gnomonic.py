"""
Gnomonic
========

The point of perspective of the gnomonic projection lies at the center of the
earth. As a consequence great circles (orthodromes) on the surface of the earth
are displayed as straight lines, which makes it suitable for distance estimation
for navigational purposes. It is neither conformal nor equal-area and the
distortion increases greatly with distance to the projection center. It follows
that the scope of application is restricted to a small area around the
projection center (at a maximum of 60°).

``flon0/lat0[/horizon]/scale`` or ``Flon0/lat0[/horizon]/width``

``lon0/lat0`` specify the projection center, the optional parameter ``horizon``
specifies the max distance from projection center (in degrees, < 90, default 60).
"""
import pygmt

fig = pygmt.Figure()
fig.coast(projection="F-90/15/4.5i", region="g", frame="20g20", land="gray")
fig.show()
