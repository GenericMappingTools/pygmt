"""
Images on figures
-----------------
The :meth:`pygmt.Figure.image` method can be used to read and place an image
file in many formats (e.g., png, jpg, eps, pdf) on a figure. We must specify
the filename via the ``imagefile`` parameter or simply use the filename as
the first argument. You can also use a full URL pointing to your desired image.
The ``position`` parameter allows us to set a reference point on the map for
the image.
"""
import os

import pygmt

fig = pygmt.Figure()
fig.basemap(region=[0, 2, 0, 2], projection="X10c", frame=True)

# place and center the GMT logo from the GMT website to the position 1/1
# on a basemap, scaled up to be 3 cm wide and draw a rectangular border
# around the image
fig.image(
    imagefile="https://www.generic-mapping-tools.org/_static/gmt-logo.png",
    position="g1/1+w3c+jCM",
    box=True,
)

# clean up the downloaded image in the current directory
os.remove("gmt-logo.png")

fig.show()
