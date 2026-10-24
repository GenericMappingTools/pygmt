r"""
Eckert IV equal-area projection
===============================

The Eckert IV projection, presented by the German cartographer Max
Eckert-Greiffendorff in 1906, is a pseudo-cylindrical equal-area projection.
Central meridian and all parallels are straight lines; other meridians are
equally spaced elliptical arcs. The scale is true along latitude 40°30'.

**kf**\ [*lon0/*]\ *scale* or **Kf**\ [*lon0/*]\ *width*

The projection is set with **kf** or **Kf**. The central meridian is set with
the optional *lon0*, and the figure size is set with *scale* or *width*.
"""

# %%
import pygmt

fig = pygmt.Figure()
# Use region "d" to specify global region (-180/180/-90/90)
fig.coast(region="d", projection="Kf12c", frame="afg", land="ivory", water="bisque4")
fig.show()
