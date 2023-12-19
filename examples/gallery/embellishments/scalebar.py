r"""
Scale bar
=========

The ``map_scale`` parameter of the :meth:`pygmt.Figure.basemap` and
:meth:`pygmt.Figure.coast` methods is used to add a scale bar to a map.
This example shows how such a scale bar can be customized:

 - position: **g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**. Set the reference
   point. Choose from

   - **g**: Give map coordinates as *longitude*\/\ *latitude*.
   - **j**\|\ **J**: Specify a two-character (order independent) code.
     Choose from vertical **T**\(op), **M**\(iddle), or **B**\(ottom) and
     horizontal **L**\(eft), **C**\(entre), or **R**\(ight). Lower / upper
     case **j** / **J** mean inside / outside of the map bounding box.
   - **n**: Give normalized bounding box coordinates as *nx*\/\ *ny*.
   - **x**: Give plot coordinates as *x*\/\ *y*.

 - length: **+w**. Give a distance value, and, optionally a distance unit.
   Choose from **e** (meters), **f** (feet), **k** (kilometers) [Default],
   **M** (statute miles), **n** (nautical miles), or **u** (US survey feet).
 - origin: **+c**\ [*slon*/]\ *slat*. Control where on the map the scale bar
   applies. If **+c** is not given the reference point is used. If only
   **+c** is appended the middle of the map is used. Note that *slon* is only
   optional for projections with constant scale along parallels, e.g.,
   Mercator projection.
 - justify: **+j**. Set the anchor point. Specify a two-character (order
   independent) code. Choose from vertical **T**\(op), **M**\(iddle), or
   **B**\(ottom) and horizontal **L**\(eft), **C**\(entre), or **R**\(ight).
 - offset: **+o**\ *offset*\|\ *xoffset*/\ *yoffset*. Give either a common
   shift or individual shifts in x (longitude) and y (latitude) directions.
 - height: Use :gmt-term:`MAP_SCALE_HEIGHT` via :func:`pygmt.config`.
 - fancy style: **+f**. Get a scale bar that looks like train tracks.
 - unit: **+u**. Add the distance unit given via **+w** to the single
   distance values.
 - label: **+l**. Add the distance unit given via **+w** as label. Append
   text to get a customized label instead.
 - alignment: **+a**. Set the label alignment. Choose from **t**\(op)
   [Default], **b**\(ottom), **l**\(eft), or **r**\(ight).
"""

# %%
import pygmt

# Create a new Figure instance
fig = pygmt.Figure()

# -----------------------------------------------------------------------------
# Add a plain scale bar
fig.basemap(
    region=[-45, -25, -15, 0],
    projection="M0/0/10c",  # Mercator projection with 10 centimeters width
    frame=["WSne", "af"],
    # The scale bar is placed at position (j) MiddleCenter, applies at the
    # reference point (+c is not given), and represents a length (+w) of 1000
    # kilometers
    map_scale="jMC+w1000k",
)

fig.shift_origin(xshift="+w1c")

# -----------------------------------------------------------------------------
# Add a fancy scale bar
fig.basemap(
    region=[-45, -25, -15, 0],
    projection="M10c",
    frame=["wSnE", "af"],
    # Place the scale bar at position (j) MiddleLeft by using MiddleLeft as
    # anchor point (+j) with an offset (+o) of 1 centimeter in x direction
    # (longitude) and 0 centimeters in y direction (latitude)
    # Use a fancy style (+f) to get a scale bar that looks like train tracks
    # Add the distance unit (+u) to the single distance values
    map_scale="jML+jML+o1c/0c+w1000k+f+u",
)

fig.show()

# %%

# Create a new Figure instance
fig = pygmt.Figure()

# -----------------------------------------------------------------------------
# Add a thick scale bar
# Adjust the GMT default parameter MAP_SCALE_HEIGHT locally (the change applies
# only to the code within the "with" block)
with pygmt.config(MAP_SCALE_HEIGHT="20p"):
    fig.basemap(
        region=[-45, -25, -15, 0],
        projection="M10c",
        frame=["WSne", "af"],
        # The scale bar applies (+c) at the middle of the map (no location is
        # appended to +c)
        # Without appending text, +l adds the distance unit as label
        map_scale="jMC+c+w1000k+f+l",
    )

fig.shift_origin(xshift="+w1c")

# -----------------------------------------------------------------------------
# Add a scale bar valid for a specific location
fig.basemap(
    region=[-45, -25, -15, 0],
    projection="M10c",
    frame=["wSnE", "af"],
    # The scale bar applies (+c) at -7° S
    # Add a customized label by appending text to +l
    map_scale="jBL+o1c/1c+c-7+w1000k+f+u+lvalid a 7° S",
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
