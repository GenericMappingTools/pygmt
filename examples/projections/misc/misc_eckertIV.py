"""
Eckert IV
=========

``Kf[central meridian]/width``: Give the optional central meridian (default is the
center of the region) and the map width.
"""
import pygmt

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(region="d", projection="Kf12c", land="ivory", water="bisque4", frame="afg")
fig.show()
