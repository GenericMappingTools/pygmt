r"""
Oblique Mercator, 2: two points
===============================

Oblique configurations of the cylinder give rise to the oblique Mercator
projection. It is particularly useful when mapping regions of large lateral
extent in an oblique direction. Both parallels and meridians are complex
curves. The projection was developed in the early 1900s by several workers.

**ob**\|\ **oB**\ *lon0/lat0/lon1/lat1/scale*\ [**+v**] or
**Ob**\|\ **OB**\ *lon0/lat0/lon1/lat1/width*\ [**+v**]

The projection is set with **o** or **O**. The pole is set in the
northern hemisphere with **b** or the southern hemisphere
with **B**. The central meridian is set by *lon0/lat0*. The oblique
equator is set by *lon1/lat1*. Align the y-axis
with the optional **+v**. The figure size is set with *scale* or *width*.
"""
import pygmt

fig = pygmt.Figure()
# Using the origin and two points
fig.coast(
    projection="Ob130/35/25/35/6c",
    # Set bottom left and top right coordinates of the figure with "+r"
    region="130/35/145/40+r",
    frame="afg",
    land="gray",
    shorelines="1/thin",
    water="lightblue",
)
fig.show()
