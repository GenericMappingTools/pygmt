"""
Universal Transverse Mercator
=============================

``U[UTM Zone/][lat0/]width``: Give UTM Zone ``UTM Zone``, and the figure width.
"""
import pygmt

fig = pygmt.Figure()
# UTM Zone is set to 52R
fig.coast(
    region=[127.5, 128.5, 26, 27],
    projection="U52R/12c",
    land="lightgreen",
    water="lightblue",
    shorelines="thinnest",
    frame="afg",
)
fig.show()
