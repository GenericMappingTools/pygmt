"""
Albers Conic Equal Area
=======================

``Blon0/lat0/lat1/lat2/width``: Give projection center ``lon0/lat0`` and two standard
parallels ``lat1/lat2``.
"""
import pygmt

fig = pygmt.Figure()
fig.coast(
    region="BR+R2", frame="afg", land="gray", borders=1, projection="B-55/-15/-25/0/8i"
)
fig.show()
