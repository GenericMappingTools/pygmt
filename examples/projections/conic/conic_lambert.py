"""
Lambert Conic Conformal Projection
==================================

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
