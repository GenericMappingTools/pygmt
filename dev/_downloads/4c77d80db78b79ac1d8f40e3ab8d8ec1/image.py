"""
Images or EPS files on maps
---------------------------
The :meth:`pygmt.Figure.image` method can be used to read and 
place a raster image file or an Encapsulated PostScript file
on a map. We must specify the file as *str* via the ``imagefile`` 
argument or simply use the filename as first argument. You can 
also use a full URL pointing to your desired image. The ``position`` 
argument allows us to set a reference point on the map for the image.

For more advanced style options, see the full option list 
at :gmt-docs:`image.html`.
"""

import pygmt

fig = pygmt.Figure()

fig.basemap(region=[0, 2, 0, 2], projection="X6c", frame=True)

# place and center the GMT logo from the GMT website to the position 1/1
# on a basemap and draw a rectangular border around the image
fig.image(
    imagefile="https://www.generic-mapping-tools.org/_static/gmt-logo.png",
    position="g1/1+w3c+jCM",
    box=True,
)

fig.show()
