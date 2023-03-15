"""
Highlight country polygons
--------------------------
The :meth:`pygmt.Figure.coast` method allows to
highlight country polygons via the ``dcw``
parameter.
"""

# sphinx_gallery_thumbnail_number = 2


import pygmt

fig = pygmt.Figure()

fig.basemap(region=[-12, 32, 34, 62], projection="M6c")

fig.coast(
    land="gray",
    water="white",
    dcw=[
        "GB+gseagreen",
        "IT+p0.75p,red3",
        "ES+p0.75p,magenta4,-",
        "RO+p1p,black,.",
        "DE+gorange+p1p,dodgerblue4",
    ],
)
fig.show()

###############################################################################
# To highlight continents instead of single countries ...

fig = pygmt.Figure()


fig.coast(
    region="d",
    projection="H10c",
    land="gray",
    water="white",
    frame="afg",
    dcw=[
        "=EU+gseagreen",
        "=AF+gred3",
        "=NA+gmagenta4",
        "=SA+gorange",
        "=AS+gdodgerblue4",
        "=OC+gtomato",
        "=AN+ggray30",
    ],
)

fig.show()
