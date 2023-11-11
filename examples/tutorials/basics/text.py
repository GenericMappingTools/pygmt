"""
Plotting text
=============

It is often useful to add text annotations to a plot or map. This is handled
by the :meth:`pygmt.Figure.text` method of the :class:`pygmt.Figure` class.
"""

import os

import numpy as np
import pygmt

# %%
# Adding a single text label
# --------------------------
#
# To add a single text label to a plot the ``text`` and ``x`` and ``y``
# parameters to specify the text and position.

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -5, 5], projection="X5c", frame=True)

fig.text(x=0, y=0, text="My text")

fig.show()


# %%
# Adjusting the text label
# ------------------------
#
# There are several optional parameters to adjust the text label:
#
# * ``font``: Sets the size, family/weight, and color of the font for the text.
#   :gmt-docs:`PostScript Fonts Used by GMT <cookbook/postscript-fonts.html>`,
#   including details of how to use non-default fonts.
# * ``angle``: Specifies the rotation of the text. It is measured counter-
#   clockwise from the horizontal in degrees.
# * ``justify``: Defines the anchor point of the bounding box for the text.
#   It is specified by a two-letter (order independent) code, chosen from:
#
#   * Vertical anchor: **T**\(op), **M**\(iddle), **B**\(ottom)
#   * Horizontal anchor: **L**\(eft), **C**\(entre), **R**\(ight)
#
# * ``offset``: Shifts the text relatively to the reference point.

fig = pygmt.Figure()

# -----------------------------------------------------------------------------
# Left: "font", "angle", and "offset" parameters
fig.basemap(region=[-5, 5, -5, 5], projection="X5c", frame="rtlb")

# Change font size, family/weight, color of the text
fig.text(x=0, y=3, text="my text", font="12p,Helvetica-Bold,blue")

# Rotate the text by 30 degrees counter-clockwise from the horizontal
fig.text(x=0, y=0, text="my text", angle=30)

# Plot marker and text label for reference
fig.plot(x=0, y=-3, style="s0.2c", fill="darkorange", pen="0.7p,darkgray")
fig.text(x=0, y=-3, text="my text")
# Shift the text label relatively to the position given via the x and y
# parameters by 1 centimeter to the right (positive x direction) and 0.5
# centimeters down (negative y direction)
fig.text(x=0, y=-3, text="my text", offset="1c/-0.5c")

fig.shift_origin(xshift="+w0.5c")

# -----------------------------------------------------------------------------
# Right: "justify" parameter
fig.basemap(region=[-1, 1, -1, 1], projection="X5c", frame="rtlb")

# Plot markers for reference
fig.plot(
    x=[-0.5, 0, 0.5, -0.5, 0, 0.5, -0.5, 0, 0.5],
    y=[0.5, 0.5, 0.5, 0, 0, 0, -0.5, -0.5, -0.5],
    style="s0.2c",
    fill="darkorange",
    pen="0.7p,darkgray",
)

# Plot text labels at the x and y positions of the markers while varying the
# anchor point via the justify parameter
fig.text(x=-0.5, y=0.5, text="TL", justify="TL")  # TopLeft
fig.text(x=0, y=0.5, text="TM", justify="TC")  # TopCenter
fig.text(x=0.5, y=0.5, text="TR", justify="TR")  # TopRight
fig.text(x=-0.5, y=0, text="ML", justify="ML")  # MiddleLeft
fig.text(x=0, y=0, text="MC", justify="MC")  # MiddleCenter
fig.text(x=0.5, y=0, text="MR", justify="MR")  # MiddleRight
fig.text(x=-0.5, y=-0.5, text="BL", justify="BL")  # BottomLeft
fig.text(x=0, y=-0.5, text="BC", justify="BC")  # BottomCenter
fig.text(x=0.5, y=-0.5, text="BR", justify="BR")  # BottomRight

fig.show()


# %%
# Adding a text box
# -----------------
#
# There are different optional parameters to add and customize a text box:
#
# * ``fill``: Fills the text box with a color.
# * ``pen``: Outlines the text box.
# * ``clearance``: Adds margins in x and y directions between the text and the
#   outline of the text box. Can be used to get a text box with rounded edges.

fig = pygmt.Figure()

fig.basemap(region=[-5, 5, -5, 5], projection="X5c", frame="rtlb")

# Add a box with a fill in green color
fig.text(x=0, y=3, text="My text", fill="green")

# Add box with a seagreen, 1-point thick, solid outline
fig.text(x=0, y=1, text="My text", pen="1p,seagreen,solid")

# Add margins between the text and the outline of the text box of 0.1
# centimeters in x direction and 0.2 centimeters in y direction
fig.text(x=0, y=-1, text="My text", pen="1p,seagreen,dashed", clearance="0.1c/0.2c")

# Get rounded edges by passing "+tO" to the "clearance" parameter
fig.text(x=0, y=-3, text="My text", pen="1p,seagreen,solid", clearance="0.2c/0.2c+tO")

fig.show()


# %%
# Adding multiple text labels with individual configurations
# ----------------------------------------------------------
#
# To add multiple text labels with individual ``font``, ``angle``, and
# ``justify`` one can provide lists with the corresponding arguments.

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -5, 5], projection="X5c", frame=True)

fig.text(
    x=[0, 0, 0],
    y=[3, 2, -2],
    font=["5p,Helvetica,black", "5p,Helvetica,blue", "6p,Courier-Bold,red"],
    angle=[0, 0, 30],
    justify=["CM", "LT", "CM"],
    text=[
        "black text with justify='CM'",
        "blue text with justify='LT'",
        "red text with angle=30",
    ],
)

fig.show()


# %%
# Using an external input file
# ----------------------------
#
# It is also possible to add text labels via an external input file containing
# ``x``, ``y``, and ``text`` columns. Addionaly, columns to set the ``angle``,
# ``front``, and ``justify`` parameters can be provided. Here, we give a
# complete example.

fig = pygmt.Figure()
fig.basemap(region=[108, 121, -5, 8], projection="M10c", frame="a2f1")
fig.coast(land="darkgray", water="steelblue", shorelines="1/0.1p,gray30")

# Create space-delimited file
with open("examples.txt", "w") as f:
    f.write("114.00  0.50   0 15p,Helvetica-Bold,white CM BORNEO\n")
    f.write("119.00  3.25   0  8p,Helvetica-Bold,black CM CELEBES SEA\n")
    f.write("112.00 -4.60   0  8p,Helvetica-Bold,black CM JAVA SEA\n")
    f.write("112.00  6.00  40  8p,Helvetica-Bold,black CM SOUTH CHINA SEA\n")
    f.write("119.12  7.25 -40  8p,Helvetica-Bold,black CM SULU SEA\n")
    f.write("118.40 -1.00  65  8p,Helvetica-Bold,black CM MAKASSAR STRAIT\n")

# Plot region names / sea names from a text file, where
# the longitude (x) and latitude (y) coordinates are in the first two columns.
# Setting angle/font/justify to True will indicate that those columns are
# present in the text file too (Please note: must be in that order).
# Finally, the text to be printed will be in the last column
fig.text(textfiles="examples.txt", angle=True, font=True, justify=True)

# Cleanups
os.remove("examples.txt")

fig.show()


# %%
# Using the position parameter
# ----------------------------
#
# Instead of using ``x`` and ``y``, the ``position`` parameter can be
# specified to set the reference point for the text on the plot.
# As for the ``justify`` parameter, the ``position`` parameter is specified
# by a two-letter (order independent) code, chosen from:
#
# * Vertical anchor: **T**\(op), **M**\(iddle), **B**\(ottom)
# * Horizontal anchor: **L**\(eft), **C**\(entre), **R**\(ight)
#
# This can be helpful to add a tag to a subplot or text labels out of
# the plot or map frame, e.g., for depth slices.

fig = pygmt.Figure()

# -----------------------------------------------------------------------------
# Left: Add a tag to a subplot
fig.basemap(region=[-5, 5, -5, 5], projection="X5c", frame=["WStr", "af"])

fig.text(
    text="(a)",
    position="TL",
    offset="0.1c/-0.1c",
    justify="TL",
)

fig.shift_origin(xshift="+w1c")

# -----------------------------------------------------------------------------
# Right: Add a text label outside of the plot or map frame

# Define region limits
lon_min = -30
lon_max = 30
lat_min = 10
lat_max = 60
# Determine projection center
lon0 = np.mean([lon_min, lon_max])
lat0 = np.mean([lat_min, lat_max])
# Determine the two standard parallels (only these two distortion-free)
lat1 = (lat_min + lat_max) / 3
lat2 = (lat_min + lat_max) / 3 * 2
# Set up arguments for the region and projection parameters
region_use = [lon_min, lon_max, lat_min, lat_max]
projection_use = (
    "L" + str(lon0) + "/" + str(lat0) + "/" + str(lat1) + "/" + str(lat2) + "/5c"
)

fig.basemap(region=region_use, projection=projection_use, frame=["lStE", "af"])

fig.text(
    text="@@100 km",  # "@@" gives "@" in GMT or PyGMT
    position="TC",
    justify="MC",
    offset="0c/0.2c",
    no_clip=True,  # Allow plotting outside of the map or plot frame
)

fig.show()


# %%
# Advanced configuration
# ----------------------
#
# For crafting more advanced styles, including using special symbols and
# other character sets, be sure to check out the GMT documentation
# at :gmt-docs:`text.html` and also the cookbook at
# :gmt-docs:`cookbook/features.html#placement-of-text`. Good luck!

# sphinx_gallery_thumbnail_number = 4
