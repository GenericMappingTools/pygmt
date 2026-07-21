r"""
Transverse Mercator projection
==============================

The transverse Mercator was invented by Johann Heinrich Lambert in 1772. In
this projection the cylinder touches a meridian along which there is no
distortion. The distortion increases away from the central meridian and goes to
infinity at 90° from center. The central meridian, each meridian 90° away from
the center, and equator are straight lines; other parallels and meridians are
complex curves.

**t**\ *lon0*\ [/\ *lat0*]/\ *scale* or **T**\ *lon0*\ [/\ *lat0*]/\ *width*

- **t** or **T**: Sets the projection type.
- *lon0*: Sets the central meridian.
- *lat0*: Sets the latitude of origin. [Optional]
- *scale* or *width*: Sets the figure size.
"""

# %%
import pygmt
from pygmt.params import Axis

fig = pygmt.Figure()
fig.coast(
    region=[20, 50, 30, 45],
    projection="T35/12c",
    frame=Axis(annot=True, tick=True, grid=True),
    land="gray80",
    water="steelblue",
)
fig.show()

# sphinx_gallery_tags = ["conformal"]
