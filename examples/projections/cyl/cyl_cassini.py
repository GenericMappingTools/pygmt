"""
Cassini Cylindrical
============================

This cylindrical projection was developed in 1745 by César-François Cassini de Thury
for the survey of France. It is occasionally called Cassini-Soldner since the latter
provided the more accurate mathematical analysis that led to the development of the
ellipsoidal formulae. The projection is neither conformal nor equal-area, and behaves
as a compromise between the two end-members. The distortion is zero along the central
meridian. It is best suited for mapping regions of north-south extent. The central
meridian, each meridian 90° away, and equator are straight lines; all other meridians
and parallels are complex curves.

**c**\ *lon0/lat0*\ */scale* or **C**\ *lon0/lat0*\ */width*

The projection is set with **c** or **C**. The projection center is set by *lon0/lat0*,
and the figure size is set with *scale* or *width*.
"""
import pygmt

fig = pygmt.Figure()
# Use the ISO code for Madagascar (MG) and pad it by 2 degrees (+R2)
fig.coast(projection="C47/-19/8i", region="MG+R2", frame="afg", land="gray", borders=1)
fig.show()
