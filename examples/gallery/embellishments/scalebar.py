r"""
Scale bar
=========

The ``map_scale`` parameter of the :meth:`pygmt.Figure.basemap` and
:meth:`pygmt.Figure.coast` methods is used to add a scale bar to a map.
This example shows how such a scale bar can be customized:

 - length: **+w**. Give value and unit.
 - origin: **+c**\ [*slon*/]\ *slat*. Note that *slon* is only optional for
   projections with constant scale along parallels, e.g., Mercator projection.
 - position: **j**. Set the reference point by specifying a two-letter (order
   independent) code, chosen from vertically **T**\(op), **M**\(iddle), or
   **B**\(ottom) and horizontally **L**\(eft), **C**\(entre), or **R**\(ight).
 - justify: **+j**. Set the anchor point by specifying a two-letter (order
   independent) code, chosen from vertically **T**\(op), **M**\(iddle), or
   **B**\(ottom) and horizontally **L**\(eft), **C**\(entre), or **R**\(ight).
 - offset: **+o**\ *offset*\|\ *xoffset*/\ *yoffset*. Give either a common
   shift or individual shifts in x (longitude) and y (latitude) directions.
 - height: Use :gmt-term:`MAP_SCALE_HEIGHT` via :func:`pygmt.config`.
 - fancy style: **+f**. Get a scale bar that looks like train tracks.
 - label: **+l**. Use another label as the unit given via **+w**.
 - label alignment: **+a**. Append **t**\(op) [Default], **b**\(ottom),
   **l**\(eft), or **r**\(ight).
 - distance unit: **+u**. Add the distance unit to the distance values.
"""

# %%
import pygmt

# Create a new Figure instance
fig = pygmt.Figure()

# -----------------------------------------------------------------------------
# Add a basic scale bar
fig.basemap(
    region=[-45, -25, -15, 0],
    projection="M0/0/10c",  # Mercator projection with 10 centimeters width
    frame=["WSne", "af"],
    # The scale bar is placed at position (j) MiddleCenter, valid at 7° S (+c),
    # and represents a length (+w) of 1000 kilometers
    map_scale="jMC+c-7+w1000k",
)

fig.shift_origin(xshift="+w1c")

# -----------------------------------------------------------------------------
# Add a fancy scale bar
fig.basemap(
    region=[-45, -25, -15, 0],
    projection="M10c",
    frame=["wSnE", "af"],
    # Place the scale bar at position MiddleLeft by using BottomLeft as anchor
    # point with an offset of 1 centimeter in x direction (longitude) and 0
    # centimeters in y direction (latitude)
    # Use a fancy style (+f) to get a scale bar that looks like train tracks
    # Add the distance unit (+u) to the single distance values
    map_scale="jML+jBL+o1c/0c+c-7+w1000k+f+u",
)

fig.show()

# %%

# Create a new Figure instance
fig = pygmt.Figure()

# -----------------------------------------------------------------------------
# Add a scale bar with a label
fig.basemap(
    region=[-45, -25, -15, 0],
    projection="M10c",
    frame=["wSnE", "af"],
    map_scale="jBL+o1c/1c+c-7+w1000k+f+u+lvalid a 7° S",
)

fig.shift_origin(xshift="+w1c")

# -----------------------------------------------------------------------------
# Add a thick scale bar
# Adjust the GMT default parameter MAP_SCALE_HEIGHT locally (the change applies
# only to the code within the "with" block)
with pygmt.config(MAP_SCALE_HEIGHT="20p"):
    fig.basemap(
        region=[-45, -25, -15, 0],
        projection="M10c",
        frame=["WSne", "af"],
        map_scale="jBL+o1c/1c+c-7+w1000k+f+u",
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

fig.coast(
    region=[-45, -25, -15, 0],
    projection="M10c",
    land="tan",
    water="steelblue",
    frame=["WSne", "af"],
    # Set the label alignment (+a) to right (r)
    map_scale="jBL+o1c/1c+c-7+w1000k+f+lkm+ar",
    # Fill the box in white with a transparency of 30 percent, add a solid
    # outline in darkgray (gray30) with a thickness of 0.5 points, and use
    # rounded edges with a radius of 3 points
    box="+gwhite@30+p0.5p,gray30,solid+r3p",
)

fig.show()

# sphinx_gallery_thumbnail_number = 3
