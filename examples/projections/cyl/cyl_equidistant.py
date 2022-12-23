r"""
Cylindrical equidistant
=======================

This simple cylindrical projection is really a linear scaling of longitudes and
latitudes. The most common form is the Plate Carrée projection, where the
scaling of longitudes and latitudes is the same. All meridians and parallels
are straight lines.

**q**\ [*lon0*/\ [*lat0*/]]\ *scale* or **Q**\ [*lon0*/\ [*lat0*/]]\ *width*

The projection is set with **q** or **Q**, and the figure size is set with
*scale* or *width*. Optionally, the central meridian can be set with *lon0*
[Default is the middle of the map]. Optionally, the standard parallel can
be set with *lat0* [Default is the equator]. When supplied, the central
meridian must be supplied as well.
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
