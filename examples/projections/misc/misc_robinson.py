"""
Robinson
========

The Robinson projection, presented by the American geographer and cartographer
Arthur H. Robinson in 1963, is a modified cylindrical projection that is neither
conformal nor equal-area. Central meridian and all parallels are straight lines; other
meridians are curved. It uses lookup tables rather than analytic expressions to make
the world map “look” right 22. The scale is true along latitudes 38. The projection was
originally developed for use by Rand McNally and is currently used by the
National Geographic Society.

``N[central meridian]/width``: Give the optional central meridian (default is the center
 of the region) and the map width.
"""
import pygmt

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(region="d", projection="N12c", land="goldenrod", water="snow2", frame="afg")
fig.show()
