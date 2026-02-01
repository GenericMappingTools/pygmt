"""
Scale bar
=========

The the :meth:`pygmt.Figure.scalebar` method can be used to add a scale bar
to a map. This example shows how such a scale bar can be customized.
"""

# %%
import pygmt
from pygmt.params import Box, Position

# Create a new Figure instance
fig = pygmt.Figure()

# Mercator projection with 10 centimeters width
fig.basemap(region=[-45, -25, -15, 0], projection="M0/0/10c", frame=["WSne", "af"])

# -----------------------------------------------------------------------------
# Top Left: Add a plain scale bar
# It is placed based on geographic coordinates (g) 42° West and 1° South,
# applies at the reference point (+c is not given), and represents a
# length (+w) of 500 kilometers
# fig.basemap(map_scale="g-42/-1+w500k")
fig.scalebar(length="500k", position=Position())

# -----------------------------------------------------------------------------
# Top Right: Add a fancy scale bar
# It is placed based on normalized bounding box coordinates (n)
# Use a fancy style (+f) to get a scale bar that looks like train tracks
# Add the distance unit (+u) to the single distance values
# fig.basemap(map_scale="n0.8/0.95+w500k+f+u")
fig.scalebar(length="500k", fancy=True, position=Position())

# -----------------------------------------------------------------------------
# Bottom Left: Add a thick scale bar
# Adjust the GMT default parameter MAP_SCALE_HEIGHT locally (the change applies
# only to the code within the "with" statement)
# It applies (+c) at the middle of the map (no location is appended to +c)
# Without appending text, +l adds the distance unit as label
with pygmt.config(MAP_SCALE_HEIGHT="10p"):
    # fig.basemap(map_scale="n0.2/0.15+c+w500k+f+l")
    fig.scalebar(
        length="500k",
        fancy=True,
        position=Position(),
    )

# -----------------------------------------------------------------------------
# Bottom Right: Add a scale bar valid for a specific location
# It is placed at BottomRight (j) using MiddleRight as anchor point (+j) with
# an offset (+o) of 1 centimeter in both x- and y-directions
# It applies (+c) at -7° South, add a customized label by appending text to +l
# fig.basemap(map_scale="jBR+jMR+o1c/1c+c-7+w500k+f+u+lvalid at 7° S")
fig.scalebar(
    length="500k",
    fancy=True,
    position=Position("BR", anchor="MR", offset=1),
)

fig.show()


# %%
# The ``box`` parameter allows surrounding the scale bar. This can be useful
# when adding a scale bar to a colorful map. To fill the box, append **+g**
# with the desired color (or pattern). The outline of the box can be adjusted
# by appending **+p** with the desired thickness, color, and style. To force
# rounded edges append **+r** with the desired radius.

# Create a new Figure instance
fig = pygmt.Figure()

fig.basemap(region=[-45, -25, -15, 0], projection="M10c", frame=["WSne", "af"])
fig.coast(land="tan", water="steelblue")
fig.scalebar(
    length="500k",
    # Set the label alignment (+a) to right (r)
    # map_scale="jBL+o1c/1c+c-7+w500k+f+lkm+ar",
    fancy=True,
    # Fill the box in white with a transparency of 30 percent, add a solid
    # outline in darkgray (gray30) with a thickness of 0.5 points, and use
    # rounded edges with a radius of 3 points
    box=Box(fill="white@30", pen="0.5p,gray30,solid", radius="3p"),
)

fig.show()

# sphinx_gallery_thumbnail_number = 1
