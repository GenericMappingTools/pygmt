r"""
Gnomonic projection
===================

The point of perspective of the gnomonic projection lies at the center of the
Earth. As a consequence great circles (orthodromes) on the surface of the Earth
are displayed as straight lines, which makes it suitable for distance
estimation for navigational purposes. It is neither conformal nor equal-area
and the distortion increases greatly with distance to the projection center. It
follows that the scope of application is restricted to a small area around the
projection center (at a maximum of 60°).

**f**\ *lon0/lat0*\ [*/horizon*]\ */scale*
or **F**\ *lon0/lat0*\ [*/horizon*]\ */width*

- **f** or **F**: Sets the projection type.
- *lon0/lat0*: Sets the projection center.
- *horizon*: Sets the maximum distance from the projection center in degrees
  (< 90°) [Optional, default is 60°].
- *scale* or *width*: Sets the figure size.
"""

# %%
import pygmt
from pygmt.params import Axis

fig = pygmt.Figure()
fig.coast(
    region="g",
    projection="F-90/15/12c",
    frame=Axis(annot=True, tick=True, grid=True),
    land="khaki",
    water="white",
)
fig.show()
