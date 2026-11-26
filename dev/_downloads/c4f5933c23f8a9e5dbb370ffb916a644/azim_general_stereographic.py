r"""
General stereographic projection
================================

This map projection is a conformal, azimuthal projection. It is mainly used
with a projection center in one of the poles. Then meridians appear as straight
lines and cross latitudes at a right angle. Unlike the azimuthal equidistant
projection, the distances in this projection are not displayed in correct
proportions. It is often used as a hemisphere map like the Lambert Azimuthal
Equal Area projection.

**s**\ *lon0/lat0*\ [*/horizon*]\ */scale*
or **S**\ *lon0/lat0*\ [*/horizon*]\ */width*

- **s** or **S**: Sets the projection type.
- *lon0/lat0*: Sets the projection center.
- *horizon*: Sets the maximum distance from the projection center in degrees
  (< 180°) [Optional, default is 90°].
- *scale* or *width*: Sets the map size.
"""

# %%
import pygmt
from pygmt.params import Axis

fig = pygmt.Figure()
fig.coast(
    region=[4, 14, 52, 57],
    projection="S0/90/12c",
    frame=Axis(annot=True, tick=True, grid=True),
    land="khaki",
    water="white",
)
fig.show()

# sphinx_gallery_tags = ["conformal"]
