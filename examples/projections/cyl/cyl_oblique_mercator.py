r"""
Oblique Mercator projection
===========================

Oblique configurations of the cylinder give rise to the oblique Mercator projection.
It is particularly useful when mapping regions of large lateral extent in an oblique
direction. Both parallels and meridians are complex curves. The projection was
developed in the early 1900s by several workers.

The projection is set with **o** or **O**. There are three different specification
ways (**a**\|\ **A**, **b**\|\ **B**, **c**\|\ **C**) available. For all three
definitions, the upper case letter mean the projection pole is set in the southern
hemisphere [Default is northern hemisphere]. Align the y-axis with the optional
modifier **+v**. The figure size is set with *scale* or *width*.


1. Using the origin and azimuth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**oa**\|\ **oA**\ *lon0/lat0/azimuth/scale*\[**+v**] or
**Oa**\|\ **OA**\ *lon0/lat0/azimuth/width*\[**+v**]

The central meridian is set by *lon0/lat0*.
The oblique equator is set by *azimuth*.


2. Using two points
~~~~~~~~~~~~~~~~~~~

**ob**\|\ **oB**\ *lon0/lat0/lon1/lat1/scale*\ [**+v**] or
**Ob**\|\ **OB**\ *lon0/lat0/lon1/lat1/width*\ [**+v**]

The central meridian is set by *lon0/lat0*.
The oblique equator is set by *lon1/lat1*.


3. Using the origin and projection pole
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**oc**\|\ **oC**\ *lon0/lat0/lonp/latp/scale*\ [**+v**] or
**Oc**\|\ **OC**\ *lon0/lat0/lonp/latp/width*\ [**+v**]

The central meridian is set by *lon0/lat0*.
The projection pole is set by *lonp/latp*.
"""

# %%
import pygmt

fig = pygmt.Figure()

# Left: Using the origin and azimuth
fig.coast(
    projection="Oa-120/25/-30/6c+v",
    # Set bottom left and top right coordinates of the figure with "+r"
    region="-122/35/-107/22+r",
    frame=["afg", "+ta | A"],
    land="gray",
)

fig.shift_origin(xshift="+w2c")

# Middle: Using two points
fig.coast(
    projection="Ob130/35/25/35/6c",
    region="130/35/145/40+r",
    frame=["afg", "+tb | B"],
    land="gray",
)

fig.shift_origin(xshift="+w2c")

# Right: Using the origin and projection pole
fig.coast(
    projection="Oc280/25.5/22/69/12c",
    region="270/20/305/25+r",
    frame=["afg", "+tc | C"],
    land="gray",
)

fig.show()
