"""
EPSG codes
==========

Besides one of the :doc:`31 projections supported by GMT </techref/projections>`, users
can pass an EPSG (European Petroleum Survey Group) code to the ``projection`` parameter.
A commonly used EPSG code is ``EPSG:3857``, that refers to the Web Mercator projection
WGS84. More information on the EPSG dataset can be found at https://epsg.org and
https://spatialreference.org/. Please note, that not all EPSG codes are supported by
GMT / PyGMT.
"""

# %%
import pygmt

fig = pygmt.Figure()

# Pass the desired EPSG code and the width of the map (separated by a slash) to the
# projection parameter
fig.basemap(region=[-180, 180, -60, 60], projection="EPSG:3857/10c", frame=30)
fig.coast(land="gray", shorelines="1/0.1p,gray10")

fig.show()
