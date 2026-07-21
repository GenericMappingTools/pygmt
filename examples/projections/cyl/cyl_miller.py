r"""
Miller cylindrical projection
=============================

This cylindrical projection, presented by Osborn Maitland Miller of the
American Geographic Society in 1942, is neither equal nor conformal. All
meridians and parallels are straight lines. The projection was designed to be a
compromise between Mercator and other cylindrical projections. Specifically,
Miller spaced the parallels by using Mercator's formula with 0.8 times the
actual latitude, thus avoiding the singular poles; the result was then divided
by 0.8.

**j**\ [*lon0/*]\ */scale* or **J**\ [*lon0/*]\ */width*

- **j** or **J**: Sets the projection type.
- *lon0*: Sets the central meridian. [Optional]
- *scale* or *width*: Sets the figure size.
"""

# %%
import pygmt
from pygmt.params import Axis

fig = pygmt.Figure()
fig.coast(
    region=[-180, 180, -80, 80],
    projection="J-65/12c",
    frame=Axis(annot=True, tick=True, grid=True),
    land="gray80",
    water="steelblue",
)
fig.show()
