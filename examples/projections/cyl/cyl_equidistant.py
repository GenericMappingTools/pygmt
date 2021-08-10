"""
Cylindrical equidistant
=======================

This simple cylindrical projection is really a linear scaling of longitudes and
latitudes. The most common form is the Plate Carrée projection, where the scaling of
longitudes and latitudes is the same. All meridians and parallels are straight lines.

**q**\ *scale* or **Q**\ *width*

The projection is set with **q** or **Q**, and the figure size is set
with *scale* or *width*.
"""
import pygmt

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(
    region="d",
    projection="Q12c",
    land="tan4",
    water="lightcyan",
    frame="afg",
)
fig.show()
