"""
EPSG codes
==========

Besides one of the :doc:`31 projections supported by GMT </techref/projections>`, users
can pass an EPSG (European Petroleum Survey Group) code to the ``projection`` parameter.
A commonly used EPSG code is ``EPSG:3857``, that refers to the Web Mercator projection
WGS84. More information on the EPSG dataset can be found at https://epsg.org/home.html.

"""

import pygmt

fig = pygmt.Figure()

fig.basemap(region=[-180, 180, -60, 60], projection="EPSG:3857/10c", frame="30")
fig.coast(shorelines="1/0.1p,gray10")

fig.show()
