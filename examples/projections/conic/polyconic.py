"""
Polyconic Projection
====================

``Poly/width``:  The only additional argument for the projection is the map width.
"""
import pygmt

fig = pygmt.Figure()
fig.coast(
    shorelines="1/0.5p",
    region=[-180, -20, 0, 90],
    projection="Poly/12c",
    land="gray",
    borders="1/thick,black",
    frame="afg10",
)

fig.show()
