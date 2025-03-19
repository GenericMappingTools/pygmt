"""
Image on a figure
=================

The :meth:`pygmt.Figure.image` method can be used to read and place an image file in
many formats (e.g., png, jpg, eps, pdf) on a figure. We must specify the filename via
the ``imagefile`` parameter or simply use the filename as the first argument. You can
also use a full URL pointing to your desired image. The ``position`` parameter allows
us to set a reference point on the map for the image.
"""

# %%

import pygmt

fig = pygmt.Figure()
fig.basemap(region=[0, 2, 0, 2], projection="X10c", frame=True)

# Place and center ("+jCM") an image provided by GMT to the position ("+g") 1/1 on a
# basemap, scaled up to be 8 cm wide ("+w") and draw a rectangular border around it
fig.image(imagefile="@needle.jpg", position="g1/1+w8c+jCM", box=True)

fig.show()
