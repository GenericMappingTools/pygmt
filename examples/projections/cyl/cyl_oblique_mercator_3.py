"""
Oblique Mercator (3)
====================

**oc**\ |**oC**\ *lon0*\ /*lat0*\ /*lonp*\ /*latp*\ /\ *scale*\ [**+v**] or
**Oc**\ |**OC**\ *lon0*\ /*lat0*\ /*lonp*\ /*latp*\ /\ *width*\ [**+v**]

"""
import pygmt

fig = pygmt.Figure()
fig.coast(
    region="125/-10/155/0+r",
    frame="afg",
    land="lightgreen",
    shorelines="1/thin",
    water="gray",
    projection="OC140/-5/106/-60/12c",
)
fig.show()
