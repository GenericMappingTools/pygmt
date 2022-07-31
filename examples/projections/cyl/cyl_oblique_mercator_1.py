r"""
Oblique Mercator, 1: origin and azimuth
=======================================

Oblique configurations of the cylinder give rise to the oblique Mercator
projection. It is particularly useful when mapping regions of large lateral
extent in an oblique direction. Both parallels and meridians are complex
curves. The projection was developed in the early 1900s by several workers.

**oa**\|\ **oA**\ *lon0/lat0/azimuth/scale*\[**+v**] or
**Oa**\|\ **OA**\ *lon0/lat0/azimuth/width*\[**+v**]

The projection is set with **o** or **O**. The pole is set in the
northern hemisphere with **a** or the southern hemisphere
with **A**. The central meridian is set by *lon0/lat0*. The oblique equator
is set by *azimuth*. Align the y-axis
with the optional **+v**. The figure size is set with *scale* or *width*.
"""
import pygmt

fig = pygmt.Figure()
# Using the origin and azimuth
fig.coast(
    projection="Oa-120/25/-30/6c+v",
    # Set bottom left and top right coordinates of the figure with "+r"
    region="-122/35/-107/22+r",
    frame="afg",
    land="gray",
    shorelines="1/thin",
    water="lightblue",
)
fig.show()
