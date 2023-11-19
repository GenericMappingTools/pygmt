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
 - offset: **+o**\ *xoffset*/*yoffset*. Shift from ``position`` in x
   (longitude) and y (latitude) directions.
 - length: **+w**\ *length*. Give value and unit.
 - height: :gmt-term:`MAP_SCALE_HEIGHT`
 - origin on map: **+c**\ [*slon*/]\ *slat*. *slon* is only optional for
   projections with constant scale along parallels.
 - fancy style: **+f**. Get a scale bar that looks like train tracks.
 - label: **+l**. Use another label as the unit given via **+w**.
 - label alignment: **+a**. Append **t**\(op) [Default], **b**\(ottom),
   **l**\(eft), or **r**\(ight).
 - distance unit: **+u**. Add the distance unit to the distance values.

Via the ``box`` parameter a box can be added around the scale bar.
"""


# %%
import pygmt

# Create a new Figure instance
fig = pygmt.Figure()

fig.basemap(
    region=[-45, -25, -15, 0],
    projection="M10c",  # Mercator projection with 10 centimeters width
    frame=["WSne", "af"],
    map_scale="jMC+w1000k",
)

fig.shift_origin(xshift="+w1c")

fig.basemap(
    region=[-45, -25, -15, 0],
    projection="M10c",
    frame=["wSnE", "af"],
    map_scale="jML+jBL+o1c/1c+w1000k+f+u",
)

fig.show()

# %%
# Amazing text

# Create a new Figure instance
fig = pygmt.Figure()

with pygmt.config(MAP_SCALE_HEIGHT="20p"):
    fig.basemap(
        region=[-45, -25, -15, 0],
        projection="M10c",
        frame=["WSne", "af"],
        map_scale="jBL+o1c/1c+w1000k+f+lkm",
    )

fig.shift_origin(xshift="+w1c")

fig.basemap(
    region=[-45, -25, -15, 0],
    projection="M10c",
    frame=["wSnE", "af"],
    map_scale="jBL+o1c/1c+c-35/-5+w1000k+f+lscale at 35° W and 5° S+ukm",
    box="+gwhite@30+p1p,gray30+r5p",
)

fig.show()

# %%
# Amazing text

# Create a new Figure instance
fig = pygmt.Figure()

fig.coast(
    region=[-45, -25, -15, 0],
    projection="M10c",
    land="tan",
    water="lightblue",
    shorelines="1/0.5p,gray30",
    frame=["WSne+gtan", "af"],
    map_scale="jBL+o1c/1c+w1000k+f+lkm+ar",
    F="+gwhite@30+p0.5p,gray30+r3p",
)

fig.show()
