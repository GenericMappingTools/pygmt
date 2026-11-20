"""
Winkel Tripel
=============

In 1921, the German mathematician Oswald Winkel a projection that was to strike a
compromise between the properties of three elements (area, angle and distance). The
German word “tripel” refers to this junction of where each of these elements are least
distorted when plotting global maps. The projection was popularized when Bartholomew
and Son started to use it in its world-renowned “The Times Atlas of the World” in the
mid-20th century. In 1998, the National Geographic Society made the Winkel Tripel as
its map projection of choice for global maps.

Naturally, this projection is neither conformal, nor equal-area. Central meridian and
equator are straight lines; other parallels and meridians are curved. The projection is
obtained by averaging the coordinates of the Equidistant Cylindrical and Aitoff
(not Hammer-Aitoff) projections. The poles map into straight lines 0.4 times the
length of equator.

**r**\ [*lon0/*]\ *scale* or **R**\ [*lon0/*]\ *width*

The projection is set with **r** or **R**. The central meridian is set with the
optional *lon0*, and the figure size is set with *scale* or *width*.
"""
import pygmt

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(region="d", projection="R12c", land="burlywood4", water="wheat1", frame="afg")
fig.show()
