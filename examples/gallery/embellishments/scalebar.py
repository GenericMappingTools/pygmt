r"""
Scale bar
=========

The ``map_scale`` parameter of the :meth:`pygmt.Figure.basemap` and
:meth:`pygmt.Figure.coast` methods is used to add a scale bar to a map.
This example shows how such a scale bar can be customized:

 - position: **j**. Set the reference point by specifying a two-letter (order
   independent) code, chosen from vertically **T**\(op), **M**\(iddle), or
   **B**\(ottom) and horizontally **L**\(eft), **C**\(entre), or **R**\(ight).
 - justify: **+j**. Set the anchor point by specifying a two-letter (order
   independent) code, chosen from vertically **T**\(op), **M**\(iddle), or
   **B**\(ottom) and horizontally **L**\(eft), **C**\(entre), or **R**\(ight).
 - offset: **+o**\ *offset*|\ *xoffset*/\ *yoffset*. Give either a common
   shift or individual shifts in x (longitude) and y (latitude) directions.
 - length: **+w**. Give value and unit.
 - height: Use :gmt-term:`MAP_SCALE_HEIGHT` via :func:`pygmt.config`.
 - origin on map: **+c**\ [*slon*/]\ *slat*. Note *slon* is only optional
   for projections with constant scale along parallels.
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
    projection="M10c",  # Mercator projection with 10 centimeters width
    frame=["WSne", "af"],
    # Place the scale bar at position MiddleCenter and let it represent a
    # length of 1000 kilometers
    map_scale="jMC+w1000k",
)

fig.shift_origin(xshift="+w1c")

# -----------------------------------------------------------------------------
# Add a fancy scale bar
fig.basemap(
    region=[-45, -25, -15, 0],
    projection="M10c",
    frame=["wSnE", "af"],
    # Place the scale bar at position MittleLeft by using BootomLeft as anchor
    # point with an offset of 1 centimeter in both x and y directions
	# Use a fancy (+f) style which looks like train tracks
	# Add the distance unit (+u) to the distance values
    map_scale="jML+jBL+o1c/1c+w1000k+f+u",
)

fig.show()

# %%

# Create a new Figure instance
fig = pygmt.Figure()

# -----------------------------------------------------------------------------
# Add a thick scale bar
# Adjust the GMT default parameter MAP_SCALE_HEIGHT locally (the change applies
# only to the code within the with block)
with pygmt.config(MAP_SCALE_HEIGHT="20p"):
    fig.basemap(
        region=[-45, -25, -15, 0],
        projection="M10c",
        frame=["WSne", "af"],
        # Instead of adding the distance unit to the distance values, give it
        # via a label (+l)
        map_scale="jBL+o1c/1c+w1000k+f+lkm",
    )

fig.shift_origin(xshift="+w1c")

# -----------------------------------------------------------------------------
# Add a scale bar for a specific origin
fig.basemap(
    region=[-45, -25, -15, 0],
    projection="M10c",
    frame=["wSnE", "af"],
    # Add a scale bar valid at 35° West and 5° South (+c)
    map_scale="jBL+o1c/1c+c-35/-5+w1000k+f+lscale at 35° W and 5° S+ukm",
)

fig.show()

# %%
# The ``box`` parameter allows surrounding the scale bar. This can be useful
# when adding a scale bar to a colorful map. The outline of the box can be
# adjusted by appending **+p** and the desired thickness, color, and style.
# To fill the box, append **+g** with the desired color (or pattern). To force
# rounded edges append **+r** with the desired radius.

# Create a new Figure instance
fig = pygmt.Figure()

fig.coast(
    region=[-45, -25, -15, 0],
    projection="M10c",
    land="tan",
    water="steelblue",
    frame=["WSne", "af"],
    # Move the label (+a) to the right (r)
    map_scale="jBL+o1c/1c+w1000k+f+lkm+ar",
	# Fill the box in white with a transparence of 30 percantage, add an
    # outline in darkgray (gray30) with a thickness of 0.5 points, and use
    # rounded edges with a radius of 3 points
    box="+gwhite@30+p0.5p,gray30+r3p",
)

fig.show()

# sphinx_gallery_thumbnail_number = 3
