"""
Transverse Mercator
===================

The transverse Mercator was invented by Johann Heinrich Lambert in 1772. In this
projection the cylinder touches a meridian along which there is no distortion. The
distortion increases away from the central meridian and goes to infinity at 90° from
center. The central meridian, each meridian 90° away from the center, and equator are
straight lines; other parallels and meridians are complex curves.

**t**\ *lon0/*\ [*lat0/*\ ]\ *scale* or **T**\ *lon0/*\ [*lat0/*\ ]\ *width*

The projection is set with **t** or **T**. The central meridian is set
by  *lon0*, the latitude of the origin is set by the optional *lat0*, and the figure
size is set with *scale* or *width*.
"""
import pygmt

fig = pygmt.Figure()
fig.coast(
    region=[20, 50, 30, 45],
    projection="T35/12c",
    land="lightbrown",
    water="seashell",
    shorelines="thinnest",
    frame="afg",
)
fig.show()
