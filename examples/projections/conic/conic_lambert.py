"""
Lambert Conic Conformal Projection
==================================

This conic projection was designed by the Alsatian mathematician Johann Heinrich
Lambert (1772) and has been used extensively for mapping of regions with predominantly
east-west orientation, just like the Albers projection. Unlike the Albers projection,
Lambert’s conformal projection is not equal-area. The parallels are arcs of circles
with a common origin, and meridians are the equally spaced radii of these circles. As
with Albers projection, it is only the two standard parallels that are distortion-free.

``Llon0/lat0/lat1/lat2/width``: Give projection center ``lon0/lat0``, two standard
parallels ``lat1/lat2``, and the map width.
"""
import pygmt

fig = pygmt.Figure()
fig.coast(
    shorelines="1/0.5p",
    region=[-130, -70, 24, 52],
    projection="L-100/35/33/45/12c",
    land="gray",
    borders=["1/thick,black", "2/thin,black"],
    frame="afg",
)

fig.show()
