"""
Cylindrical equidistant
=======================

``Qwidth``: Give the figure ``width``.
"""
import pygmt

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(
    region="d",
    projection="Q12c",
    land="tan4",
    water="lightcyan",
    frame="afg",
)
fig.show()
