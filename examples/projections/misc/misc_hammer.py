"""
Hammer projection
=================

``H[central meridian]/width``: Give the optional central meridian (default is 180)
and the map width.
"""
import pygmt

fig = pygmt.Figure()
# Use region "g" to specify global region
fig.coast(region="g", projection="H12c", land="black", water="cornsilk", frame="afg")
fig.show()

fig = pygmt.Figure()
# Add the optional central meridian argument (in this example, 0 degrees latitude)
fig.coast(region="g", projection="H0/12c", land="black", water="cornsilk", frame="afg")
fig.show()