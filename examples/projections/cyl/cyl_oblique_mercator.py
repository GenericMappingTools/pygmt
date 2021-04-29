"""
Oblique Mercator
================

Oblique configurations of the cylinder give rise to the oblique Mercator
projection. It is particularly useful when mapping regions of large lateral
extent in an oblique direction. Both parallels and meridians are complex
curves. The projection was developed in the early 1900s by several workers.

**o**\ **a**\ *lon0/lat0* */azimuth*\ */scale*\ **[+v]** or
**O**\ **A**\ *lon0/lat0* */azimuth*\ */width*\ **[+v]** or

**o**\ **b**\ *lon0/lat0* */lon1/lat1*\ */scale*\ **[+v]** or
**O**\ **B**\ *lon0/lat0* */lon1/lat1*\ */width*\ **[+v]** or

**o**\ **c**\ *lon0/lat0* */lonp/latp*\ */scale*\ **[+v]** or
**O**\ **C**\ *lon0/lat0* */lonp/latp*\ */width*\ **[+v]**

The projection is set with **o** or **O**. The central meridian is set by
*lon0/lat0*. The oblique equator is set by the azimuth in option one.
The oblique equator is set by *lon1/lat1* in option two. The projection
pole is set by *lonp/latp* in option three. Align the y-axis with the
optional *+v*. The figure size is set with *scale* or *width*.
"""
import pygmt

fig = pygmt.Figure()

# Option 1 using the origin and azimuth
fig.coast(projection="Oa-120/25/-120/12c+v",
    region= [-122, -107, 22, 35],
    frame="afg",
    land="gray",
    water="lightblue",
    )
fig.show()

# Option 2 using the origin and two points
fig.coast(projection="Ob138/36/305/25/12c",
    region= "JP",
    frame="afg",
    land="gray",
    water="lightblue",
    )
fig.show()


# Option 3 using the origin projection pole
fig.coast(projection="Oc280/25.5/22/69/12c",
    region= [270, 305, 20, 35],
    frame="afg",
    land="gray",
    water="lightblue",
    )
fig.show()
