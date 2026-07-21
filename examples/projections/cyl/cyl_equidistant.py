r"""
Cylindrical equidistant projection
==================================

This simple cylindrical projection is really a linear scaling of longitudes and
latitudes. The most common form is the Plate Carrée projection, where the
scaling of longitudes and latitudes is the same. All meridians and parallels
are straight lines.

**q**\ [*lon0*/\ [*lat0*/]]\ *scale* or **Q**\ [*lon0*/\ [*lat0*/]]\ *width*

- **q** or **Q**: Sets the projection type.
- *lon0*: Sets the central meridian [Optional, default is the middle of the map].
- *lat0*: Sets the standard parallel. When supplied, *lon0* must be supplied as
  well. [Optional, default is the equator].
- *scale* or *width*: Sets the figure size.
"""

# %%
import pygmt
from pygmt.params import Axis

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(
    region="d",
    projection="Q12c",
    frame=Axis(annot=True, tick=True, grid=True),
    land="gray80",
    water="steelblue",
)
fig.show()

# sphinx_gallery_tags = ["equidistant"]
