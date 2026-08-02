r"""
Equidistant conic projection
============================

The equidistant conic projection was described by the Greek philosopher
Claudius Ptolemy about A.D. 150. It is neither conformal or equal-area, but
serves as a compromise between them. The scale is true along all meridians and
the standard parallels.

**d**\ *lon0/lat0*\ /\ *lat1/lat2*\ */scale*
or **D**\ *lon0/lat0*\ /\ *lat1/lat2*\ */width*

- **d** or **D**: Sets the projection type.
- *lon0/lat0*: Sets the projection center.
- *lat1/lat2*: Sets the two standard parallels.
- *scale* or *width*: Sets the map size.
"""

# %%
import pygmt
from pygmt.params import Axis

fig = pygmt.Figure()
fig.coast(
    region=[-88, -70, 18, 24],
    projection="D-79/21/19/23/12c",
    frame=Axis(annot=True, tick=True, grid=True),
    land="seagreen",
    water="gray90",
)
fig.show()

# sphinx_gallery_tags = ["equidistant"]
