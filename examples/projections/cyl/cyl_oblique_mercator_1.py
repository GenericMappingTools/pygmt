"""
Oblique Mercator (1)
====================

**oa**\ |**oA**\ *lon0*\ /*lat0*\ /\ *azim*/*scale*\ [**+v**] or
**Oa**\ |**OA**\ *lon0*\ /*lat0*\ /\ *azim*/*width*\ [**+v**]

"""
import pygmt

fig = pygmt.Figure()
fig.coast(
    region="-90/20/-55/25+r",
    frame="afg",
    land="red",
    water="cyan",
    resolution="i",
    projection="Oa280/25.5/-60/12c",
)
fig.show()
