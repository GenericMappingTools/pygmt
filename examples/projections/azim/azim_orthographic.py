r"""
Orthographic projection
=======================

This is a perspective projection like the general perspective, but with the
difference that the point of perspective lies in infinite distance.
It is therefore often used to give the appearance of a globe viewed from outer
space, were one hemisphere can be seen as a whole. It is neither conformal nor
equal-area and the distortion increases near the edges.

**g**\ *lon0/lat0*\ [*/horizon*]\ */scale*
or **G**\ *lon0/lat0*\ [*/horizon*]\ */width*

- **g** or **G**: Sets the projection type.
- *lon0/lat0*: Sets the projection center.
- *horizon*: Sets the maximum distance from the projection center in degrees
  (<= 90°) [Optional, default is 90°].
- *scale* or *width*: Sets the figure size.
"""

# %%
import pygmt
from pygmt.params import Axis

fig = pygmt.Figure()
fig.coast(
    region="g",
    projection="G10/52/12c",
    frame=Axis(annot=True, tick=True, grid=True),
    land="khaki",
    water="white",
)
fig.show()
