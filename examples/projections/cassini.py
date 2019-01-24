"""
Cassini Cylindrical
============================

``Clon0/lat0/width``: ``lon0`` and ``lat0`` specifies the projection center.
"""
import pygmt

fig = pygmt.Figure()
fig.coast(region="MG+R2", frame="afg", land="gray", borders=1, projection="C47/-19/8i")
fig.show()
