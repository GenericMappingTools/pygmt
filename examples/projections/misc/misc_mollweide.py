r"""
Mollweide projection
====================

This pseudo-cylindrical, equal-area projection was developed by the German
mathematician and astronomer Karl Brandan Mollweide in 1805. Parallels are
unequally spaced straight lines with the meridians being equally spaced
elliptical arcs. The scale is only true along latitudes 40°44' north and south.
The projection is used mainly for global maps showing data distributions. It is
occasionally referenced under the name homalographic projection.

**w**\ [*lon0/*]\ *scale* or **W**\ [*lon0/*]\ *width*

- **w** or **W**: Sets the projection type.
- *lon0*: Sets the central meridian. [Optional]
- *scale* or *width*: Sets the figure size.
"""

# %%
import pygmt
from pygmt.params import Axis

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(
    region="d",
    projection="W12c",
    frame=Axis(annot=True, tick=True, grid=True),
    land="ivory",
    water="bisque4",
)
fig.show()

# sphinx_gallery_tags = ["equal-area"]
