"""
Focal mechanisms
----------------

The :meth:`pygmt.Figure.meca` method can plot focal mechanisms, or beachballs.
We must specify the focal mechanism nodal planes or moment tensor components as
columns using the ``spec`` argument, and the size of plotted beachballs using the 
``scale`` argument.
"""

import pygmt

fig = pygmt.Figure()

# generate a basemap near Washington state showing coastlines, land, and water
fig.coast(region=[-125, -122, 47, 49], projection='M6c', land='grey', water='lightblue',
            shorelines=True, resolution='f', frame='a')

# store focal mechanisms parameters in a dict
focal_mechanisms = dict(strike=330, dip=30, rake=90, magnitude=3)

# pass the focal mechanism data to meca in addition to the scale and event location
fig.meca(focal_mechanisms, scale='1c', lon=-124.3, lat=48.1, depth=12.0)

fig.show()