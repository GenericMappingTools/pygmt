r"""
Azimuthal equidistant projection
================================

The main advantage of this projection is that distances from the projection
center are displayed in correct proportions. Also directions measured from the
projection center are correct. It is very useful for a global view on locations
that lie within a certain distance or for comparing distances of different
locations relative to the projection center.

**e**\ *lon0/lat0*\ [*/horizon*]\ */scale* or
**E**\ *lon0/lat0*\ [*/horizon*]\ */width*

- **e** or **E**: Sets the projection type.
- *lon0/lat0*: Sets the projection center.
- *horizon*: The maximum distance from the projection center to the edge of the
  map (i.e. the visible portion of the rest of the world map) in degrees
  (<= 180°) [Optional, default is 180°].
- *scale* or *width*: Sets the map size.
"""

# %%
import pygmt
from pygmt.params import Axis

fig = pygmt.Figure()
fig.coast(
    region="g",
    projection="E-100/40/15c",
    frame=Axis(annot=True, tick=True, grid=True),
    land="khaki",
    water="white",
)
fig.show()

# sphinx_gallery_tags = ["equidistant"]
