r"""
Eckert IV equal-area projection
===============================

The Eckert IV projection, presented by the German cartographer Max
Eckert-Greiffendorff in 1906, is a pseudo-cylindrical equal-area projection.
Central meridian and all parallels are straight lines; other meridians are
equally spaced elliptical arcs. The scale is true along latitude 40°30'.

**kf**\ [*lon0/*]\ *scale* or **Kf**\ [*lon0/*]\ *width*

- **kf** or **Kf**: Sets the projection type.
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
    projection="Kf12c",
    frame=Axis(annot=True, tick=True, grid=True),
    land="ivory",
    water="bisque4",
)
fig.show()

# sphinx_gallery_tags = ["equal-area"]
