"""
Cassini Cylindrical
============================

``Clon0/lat0/width``: ``lon0`` and ``lat0`` specifies the projection center.
"""
import pygmt

fig = pygmt.Figure()
# Use the ISO code for Madagascar (MG) and pad it by 2 degrees (+R2)
fig.coast(projection="C47/-19/8i", region="MG+R2", frame="afg", land="gray", borders=1)
fig.show()
