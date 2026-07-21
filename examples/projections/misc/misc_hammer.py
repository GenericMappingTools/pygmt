r"""
Hammer projection
=================

The equal-area Hammer projection, first presented by the German mathematician
Ernst von Hammer in 1892, is also known as Hammer-Aitoff (the Aitoff projection
looks similar, but is not equal-area). The border is an ellipse, equator and
central meridian are straight lines, while other parallels and meridians are
complex curves.

**h**\ [*lon0/*]\ *scale* or **H**\ [*lon0/*]\ *width*

- **h** or **H**: Sets the projection type.
- *lon0*: Sets the central meridian. [Optional]
- *scale* or *width*: Sets the map size.
"""

# %%
import pygmt
from pygmt.params import Axis

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(
    region="d",
    projection="H12c",
    frame=Axis(annot=True, tick=True, grid=True),
    land="ivory",
    water="bisque4",
)
fig.show()

# sphinx_gallery_tags = ["equal-area"]
