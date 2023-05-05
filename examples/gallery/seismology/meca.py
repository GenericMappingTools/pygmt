"""
Focal mechanisms
----------------

The :meth:`pygmt.Figure.meca` method can plot focal mechanisms or beachballs.
We can specify the focal mechanism nodal planes or moment tensor components
as a dictionary using the ``spec`` parameter (or they can be specified as a
1-D or 2-D array, or within a file). The size of the beachballs can be set
using the ``scale`` parameter. The compressive and extensive quadrants can
be filled either with a color or a pattern via the ``compressionfill`` and
``extensionfill`` parameters, respectively. Use the ``pen`` parameter to
adjust the outline of the beachballs.
"""

import pygmt

fig = pygmt.Figure()

# Generate a map near Washington State showing land, water, and shorelines
fig.coast(
    region=[-125, -122, 47, 49],
    projection="M6c",
    land="grey",
    water="lightblue",
    shorelines=True,
    frame="a",
)

# Store focal mechanism parameters in a dictionary based on the Aki & Richards
# convention
focal_mechanism = dict(strike=330, dip=30, rake=90, magnitude=3)

# Pass the focal mechanism data through the spec parameter. In addition provide
# scale, event location, and event depth
fig.meca(
    spec=focal_mechanism,
    scale="1c",  # in centimeters
    longitude=-124.3,
    latitude=48.1,
    depth=12.0,
    # Fill compressive quadrants with color "red"
    # [Default is "black"]
    compressionfill="red",
    # Fill extensive quadrants with color "cornsilk"
    # [Default is "white"]
    extensionfill="cornsilk",
    # Draw a 0.5 points thick dark gray ("gray30") solid outline via
    # the pen parameter [Default is "0.25p,black,solid"]
    pen="0.5p,gray30,solid",
)

fig.show()
