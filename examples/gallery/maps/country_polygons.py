"""
Highlight country and continent polygons
----------------------------------------
The :meth:`pygmt.Figure.coast` method can
highlight country polygons via the ``dcw``
parameter. It accepts the country code, and
can draw its borders and add a color to its landmass.
"""

# sphinx_gallery_thumbnail_number = 2


import pygmt

fig = pygmt.Figure()

fig.basemap(
    region=[-12, 32, 34, 62],
    projection="M6c",
    frame=True,
)

fig.coast(
    land="gray",
    water="white",
    dcw=[
        # Great Britain with seagrean land
        "GB+gseagreen",
        # Italy with a red border
        "IT+p0.75p,red3",
        # Spain with a magenta dashed border
        "ES+p0.75p,magenta4,-",
        # Romania with a black dotted border
        "RO+p1p,black,.",
        # Germany with orange land and a blue border
        "DE+gorange+p1p,dodgerblue4",
    ],
)
fig.show()

###############################################################################
# Entire continents can also be highlighted by adding ``"="`` in
# front of the continent code to differentiate it from a country code.

fig = pygmt.Figure()

fig.coast(
    region="d",
    projection="H10c",
    land="gray",
    water="white",
    frame="afg",
    dcw=[
        # Europe
        "=EU+gseagreen",
        # Africa
        "=AF+gred3",
        # North America
        "=NA+gmagenta4",
        # South America
        "=SA+gorange",
        # Asia
        "=AS+gdodgerblue4",
        # Oceania
        "=OC+gtomato",
        # Antarctica
        "=AN+ggray30",
    ],
)

fig.show()
