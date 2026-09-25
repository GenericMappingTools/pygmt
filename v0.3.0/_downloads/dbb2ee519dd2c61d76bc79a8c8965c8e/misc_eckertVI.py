"""
Eckert VI
=========

The Eckert VI projections, presented by the German cartographer
Max Eckert-Greiffendorff in 1906, is a pseudo-cylindrical equal-area projection.
Central meridian and all parallels are straight lines; other meridians are equally
spaced sinusoids. The scale is true along latitude 49°16’.


**ks**\ [*lon0/*]\ *scale* or **Ks**\ [*lon0/*]\ *width*

The projection is set with **ks** or **Ks**. The central meridian is set with the
optional *lon0*, and the figure size is set with *scale* or *width*.
"""
import pygmt

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(region="d", projection="Ks12c", land="ivory", water="bisque4", frame="afg")
fig.show()
