"""
Eckert IV
=========

The Eckert IV projection, presented by the German cartographer Max
Eckert-Greiffendorff in 1906, is a pseudo-cylindrical equal-area projection. Central
meridian and all parallels are straight lines; other meridians are equally spaced
elliptical arcs. The scale is true along latitude 40°30’.

``Kf[central meridian]/width``: Give the optional central meridian (default is the
center of the region) and the map width.
"""
import pygmt

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(region="d", projection="Kf12c", land="ivory", water="bisque4", frame="afg")
fig.show()
