"""
Oblique Mercator (2)
====================


**Ob**\ |lon0|/|lat0|/|lon1|/|lat1|/\ *width*\ [**+v**]

"""
import pygmt

fig = pygmt.Figure()
fig.coast(
    region="23/34.5/26.5/36+r",
    frame="afg",
    land="darkgreen",
    water="lightgray",
    resolution="i",
    projection="Ob23/34/24/34/12c",
)
fig.show()
