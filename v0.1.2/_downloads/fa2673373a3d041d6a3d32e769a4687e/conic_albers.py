"""
Albers Conic Equal Area
=======================

``Blon0/lat0/lat1/lat2/width``: Give projection center ``lon0/lat0`` and two standard
parallels ``lat1/lat2``.
"""
import pygmt

fig = pygmt.Figure()
# Use the ISO country code for Brazil and add a padding of 2 degrees (+R2)
fig.coast(
    projection="B-55/-15/-25/0/8i", region="BR+R2", frame="afg", land="gray", borders=1
)
fig.show()
