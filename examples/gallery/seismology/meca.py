"""
Focal mechanisms
----------------

The :meth:`pygmt.Figure.meca` method can plot focal mechanisms or beachballs.
We can specify the focal mechanism nodal planes or moment tensor components as
a dictionary using the ``spec`` parameter (or they can be specified as a 1-D
or 2-D array, or within a specified file). The size of plotted beachballs can
be specified using the ``scale`` parameter.
"""

import pygmt

fig = pygmt.Figure()

# generate a map near Washington State showing land, water, and shorelines
fig.coast(
    region=[-125, -122, 47, 49],
    projection="M6c",
    land="grey",
    water="lightblue",
    shorelines=True,
    frame="a",
)

# store focal mechanism parameters in a dictionary based on the Aki & Richards
# convention
focal_mechanism = dict(strike=330, dip=30, rake=90, magnitude=3)

# pass the focal mechanism data through the spec parameter. In addition provide
# scale, event location, and event depth
fig.meca(
    spec=focal_mechanism,
    scale="1c",  # in centimeters
    longitude=-124.3,
    latitude=48.1,
    depth=12.0,
)

fig.show()
