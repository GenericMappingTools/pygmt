r"""
Using EPSG codes to specify projection
===============================

The EPSG registry is a public registry of geodetic datums, spatial reference systems,
Earth ellipsoids, coordinate transformations and related units of measurement.

These are used frequently in GIS software and data. If data are plotted using a linear
projection, additional features (e.g. coast) can be made congruent by specifying EPSG.
See Gallery Example "RGB Image"

Some common EPSG codes are:

EPSG:4326 - WGS 84 - latitude/longitude coordinate system based on the Earth's centre
of mass, used by the Global Positioning System among others.

EPSG:3857 - Web Mercator - used for display by many web-based mapping tools, including
Google Maps and OpenStreetMap.


**[EPSG:XXXX]**

"""

import pygmt

fig = pygmt.Figure()
fig.coast(
    region=[-180, 180, -80, 80], projection="EPSG:3857", frame=True, shorelines="1p"
)
fig.show()
