"""
Lambert Azimuthal Equal Area
============================

``Alon0/lat0[/horizon]/width``: ``lon0`` and ``lat0`` specifies the projection center.
``horizon`` specifies the max distance from projection center (in degrees, <= 180,
default 90).
"""
import pygmt

fig = pygmt.Figure()
fig.coast(region="g", frame="afg", land="gray", projection="A30/-20/60/8i")
fig.show()
