r"""
Robinson projection
===================

The Robinson projection, presented by the American geographer and cartographer
Arthur H. Robinson in 1963, is a modified cylindrical projection that is
neither conformal nor equal-area. Central meridian and all parallels are
straight lines; other meridians are curved. It uses lookup tables rather than
analytic expressions to make the world map "look" right [#f1]_.
The scale is true along latitudes 38° north and south. The projection was
originally developed for use by Rand McNally and is currently used by the
National Geographic Society.

**n**\ [*lon0/*]\ *scale* or **N**\ [*lon0/*]\ *width*

- **n** or **N**: Sets the projection type.
- *lon0*: Sets the central meridian. [Optional]
- *scale* or *width*: Sets the figure size.

.. rubric:: Footnotes

.. [#f1] Robinson provided a table of y-coordinates for latitudes every 5°.
         To project values for intermediate latitudes one must interpolate
         the table. Different interpolants may result in slightly different
         maps. GMT uses the interpolant selected by the parameter
         :gmt-term:`GMT_INTERPOLANT` in the gmt.conf file.
"""

# %%
import pygmt
from pygmt.params import Axis

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(
    region="d",
    projection="N12c",
    frame=Axis(annot=True, tick=True, grid=True),
    land="ivory",
    water="bisque4",
)
fig.show()
