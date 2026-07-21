r"""
Van der Grinten projection
==========================

The Van der Grinten projection, presented by Alphons J. van der Grinten in
1904, is neither equal-area nor conformal. Central meridian and Equator are
straight lines; other meridians are arcs of circles. The scale is true along
the Equator only. Its main use is to show the entire world enclosed in a
circle.

**v**\ [*lon0/*]\ *scale* or **V**\ [*lon0/*]\ *width*

- **v** or **V**: Sets the projection type.
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
    projection="V12c",
    frame=Axis(annot=True, tick=True, grid=True),
    land="ivory",
    water="bisque4",
)
fig.show()
