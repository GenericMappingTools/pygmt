"""
Mercator
========

``M[lon0/][lat0/]width``: Give central meridian ``lon0`` (optional) and
standard parallel ``lat0`` (optional).
"""
import pygmt

fig = pygmt.Figure()
fig.coast(region=[0, 360, -80, 80], frame="afg", land="gray", projection="M0/0/8i")
fig.show()
