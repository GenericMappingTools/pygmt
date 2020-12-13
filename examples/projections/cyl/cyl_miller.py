"""
Miller cylindrical
==================

``J[lon0/]width``: Give the optional central meridian ``lon0`` and the figure ``width``.
"""
import pygmt

fig = pygmt.Figure()
fig.coast(
    region=[-180, 180, -80, 80],
    projection="J-65/12c",
    land="khaki",
    water="azure",
    shorelines="thinnest",
    frame="afg",
)
fig.show()
