r"""
Oblique Mercator, 3: origin and pole
====================================

Oblique configurations of the cylinder give rise to the oblique Mercator
projection. It is particularly useful when mapping regions of large lateral
extent in an oblique direction. Both parallels and meridians are complex
curves. The projection was developed in the early 1900s by several workers.

**oc**\|\ **oC**\ *lon0/lat0/lonp/latp/scale*\ [**+v**] or
**Oc**\|\ **OC**\ *lon0/lat0/lonp/latp/width*\ [**+v**]

The projection is set with **o** or **O**. The central meridian is set
by *lon0/lat0*. The projection pole is set by *lonp/latp* in option three.
Align the y-axis with the optional **+v**. The figure size is set
with *scale* or *width*.
"""
import pygmt

fig = pygmt.Figure()
# Using the origin and projection pole
fig.coast(
    projection="Oc280/25.5/22/69/12c",
    # Set bottom left and top right coordinates of the figure with "+r"
    region="270/20/305/25+r",
    frame="afg",
    land="gray",
    shorelines="1/thin",
    water="lightblue",
)
fig.show()
