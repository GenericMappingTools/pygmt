"""
Oblique Mercator
================

Oblique configurations of the cylinder give rise to the oblique Mercator
projection. It is particularly useful when mapping regions of large lateral
extent in an oblique direction. Both parallels and meridians are complex
curves. The projection was developed in the early 1900s by several workers.

**oa**\ *lon0/lat0* */azimuth*\ */scale*\ **[+v]** or
**OA**\ *lon0/lat0* */azimuth*\ */width*\ **[+v]** or

**ob**\ *lon0/lat0* */lon1/lat1*\ */scale*\ **[+v]** or
**OB**\ *lon0/lat0* */lon1/lat1*\ */width*\ **[+v]** or

**oc**\ *lon0/lat0* */lonp/latp*\ */scale*\ **[+v]** or
**OC**\ *lon0/lat0* */lonp/latp*\ */width*\ **[+v]**

The projection is set with **o** or **O**. The central meridian is set by
*lon0/lat0*. The oblique equator is set by the azimuth in option one.
The oblique equator is set by *lon1/lat1* in option two. The projection
pole is set by *lonp/latp* in option three. Align the y-axis with the
optional *+v*. The figure size is set with *scale* or *width*.
"""
import pygmt

fig = pygmt.Figure()

# Option 1 using the origin and azimuth
fig.coast(projection="Oa-120/25/-30/12c+v",
    region= "-122/35/-107/22+r",
    frame="afg",
    land="gray",
    water="lightblue",
    )
fig.show()

# Option 2 using the origin and two points
fig.coast(projection="Ob130/35/25/35/12c",
    region= "130/35/145/40+r",
    frame="afg",
    land="gray",
    water="lightblue",
    )
fig.show()

# Option 3 using the origin projection pole
fig.coast(projection="Oc280/25.5/22/69/12c",
    region= "270/20/305/25+r",
    frame="afg",
    land="gray",
    water="lightblue",
    )
fig.show()
