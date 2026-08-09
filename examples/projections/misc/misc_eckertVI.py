r"""
Eckert VI equal-area projection
===============================

The Eckert VI projections, presented by the German cartographer Max
Eckert-Greiffendorff in 1906, is a pseudo-cylindrical equal-area projection.
Central meridian and all parallels are straight lines; other meridians are
equally spaced sinusoids. The scale is true along latitude 49°16'.


**ks**\ [*lon0/*]\ *scale* or **Ks**\ [*lon0/*]\ *width*

- **ks** or **Ks**: Sets the projection type.
- *lon0*: Sets the central meridian [Optional].
- *scale* or *width*: Sets the map size.
"""

# %%
import pygmt
from pygmt.params import Axis

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(
    region="d",
    projection="Ks12c",
    frame=Axis(annot=True, tick=True, grid=True),
    land="ivory",
    water="bisque4",
)
fig.show()

# sphinx_gallery_tags = ["equal-area"]
