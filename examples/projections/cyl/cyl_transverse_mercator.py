"""
Transverse Mercator
===================

The transverse Mercator was invented by Johann Heinrich Lambert in 1772. In this
projection the cylinder touches a meridian along which there is no distortion. The
distortion increases away from the central meridian and goes to infinity at 90° from
center. The central meridian, each meridian 90° away from the center, and equator are
straight lines; other parallels and meridians are complex curves.

``T[lon0/][lat0/]width``: Give central meridian ``lon0``, the latitude of the
origin ``lat0`` (optional), and the figure width.
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
