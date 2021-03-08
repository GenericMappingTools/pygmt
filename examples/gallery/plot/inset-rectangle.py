"""
Inset with an rectangle
------------------------

The :meth:`pygmt.Figure.inset` method adds an inset figure inside a larger
figure. The function is called using a ``with`` statement, and its position,
box, offset, and margin parameters are set. Plotting methods called within the
``with`` statement plot into the inset figure.
"""

import numpy as np
import pygmt
from pygmt.helpers import GMTTempFile

# Set the region to be near Tokyo
region = np.array([139.2, 140.5, 34.8, 36])

fig = pygmt.Figure()

# Plot the base map of the primary figure
fig.basemap(
    region=region,
    projection="M12c",
    frame=["WSne", "af"],
)

# Set the land color to "lightbrown", the water to "azure1", the shorelines
# width to "2p", the smallest area to 1000 km2 for the primary figure
fig.coast(
    land="lightbrown",
    water="azure1",
    shorelines="2p",
    area_thresh=1000,
)

# Create an inset, setting the position to bottom left, the width to
# 3 centimeters, the height to 3.6 centimeters, and  the x- and y-offsets to
# 0.2 centimeters. Draws a rectangular box around the inset with a fill color
# of "white" and a pen of "1p".
with fig.inset(position="jBL+w3c/3.6c+o0.1c", box="+gwhite+p1p"):
    # Plot the Japan main land in the inset using coast
    # "M?" means Mercator projection with map width automatically determined
    # based on the width in the position parameter of inset.
    fig.coast(
        region=[129, 146, 30, 46],
        projection="M?",
        dcw="JP+glightbrown+p0.2p",
        area_thresh=10000,
    )
    # Plot a rectangle in the inset map to show the area of the primary figure
    with GMTTempFile() as temp_file:
        with open(temp_file.name, "w") as f:
            f.write("{} {} {} {}".format(region[0], region[2], region[1], region[3]))
        fig.plot(
            data=temp_file.name,
            style="r+s",
            pen="1p,blue",
        )

fig.show()
