"""
Winkel Tripel
=============

``R[central meridian]/width``: Give the optional central meridian (default is the center
 of the region) and the map width.
"""
import pygmt

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(region="d", projection="R12c", land="burlywood4", water="wheat1", frame="afg")
fig.show()
