r"""
Lambert azimuthal equal-area projection
=======================================

This projection was developed by Johann Heinrich Lambert in 1772 and is
typically used for mapping large regions like continents and hemispheres. It is
an azimuthal, equal-area projection, but is not perspective. Distortion is zero
at the center of the projection, and increases radially away from this point.

**a**\ *lon0/lat0*\ [*/horizon*]\ */scale*
or **A**\ *lon0/lat0*\ [*/horizon*]\ */width*

- **a** or **A**: Sets the projection type.
- *lon0/lat0*: Sets the projection center.
- *horizon*: Sets the maximum distance from the projection center in degrees
  (<= 180°) [Optional, default is 90°].
- *scale* or *width*: Sets the figure size.
"""

# %%
import pygmt
from pygmt.params import Axis

fig = pygmt.Figure()
fig.coast(
    region="g",
    projection="A30/-20/60/12c",
    frame=Axis(annot=True, tick=True, grid=True),
    land="khaki",
    water="white",
)
fig.show()

# sphinx_gallery_tags = ["equal-area"]
