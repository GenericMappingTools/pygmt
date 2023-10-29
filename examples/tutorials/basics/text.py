"""
Plotting text
=============

It is often useful to add annotations to a plot. This is handled by the
:meth:`pygmt.Figure.text` method of the :class:`pygmt.Figure` class.
"""

import os

import numpy as np
import pygmt

# %%
# Add a single text label
# -----------------------
#
# To add a single text label to a plot or map the ``text``, ``x``, and ``y``
# parameters to specify the text and position within the plot frame.

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -5, 5], projection="X5c", frame="af")

fig.text(text="My text", x=0, y=0)

fig.show()


# %%
# Adjust text labels
# ------------------
#
# The size, family/weight, and color of an annotation can be specified using
# the ``font`` parameter. A list of all recognized fonts can be found at
# :gmt-docs:`PostScript Fonts Used by GMT <cookbook/postscript-fonts.html>`,
# including details of how to use non-default fonts.
# The ``angle`` parameter is used to specify the counter-clockwise rotation in
# degrees of the text from the horizontal.
# The ``justify`` parameter is used to define the anchor point for the bounding
# box for the text. it is specified by a two-letter (order independent) code,
# chosen from:
#
# * Vertical anchor: **T**\(op), **M**\(iddle), **B**\(ottom)
# * Horizontal anchor: **L**\(eft), **C**\(entre), **R**\(ight)
#
# The ``offset`` parameter can be used to shift the text label relative to the
# reference point. This can be used full when adding labels to data points.
#
# The ``fill`` parameter is used to set the fill color of the area surrounding
# the text. Add an outline to the text box via the ``pen`` parameter. The add
# a margin between the text and the box as well as to force rounded corner the
# ``clearance`` parameter can be used.

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -5, 5], projection="X5c", frame=["WSte", "af"])

# Change font size, family/weight, color
fig.text(x=0, y=2, text="My Text", font="12p,Helvetica-Bold,blue")
# Rotate text by 30 degrees counter-clockwise from the horizontal
fig.text(x=0, y=0, text="My Text", angle=30)
# Set the anchor point to TopLeft
fig.text(x=0, y=-2, text="My Text", justify="TL")
# Offset text by 0.2 centimeters in x and y-directions
fig.text(x=0, y=-4, text="My Text", offset="1c/-0.2c")

# -----------------------------------------------------------------------------
fig.shift_origin(xshift="+w0.5c")

fig.basemap(region=[-5, 5, -5, 5], projection="X5c", frame=["wStr", "af"])

# Add box with green fill
fig.text(x=0, y=2, text="My text", fill="green")
# Add box with an darkgreen, 0.5 points thick outline
fig.text(x=0, y=0, text="My text", pen="0.5p,darkgreen")
# Add box with a margin in x and y directions
fig.text(x=0, y=-2, text="My text", pen="0.5p,darkgreen", clearance="0.2c/0.2c")
# Add outline with roundet corners
fig.text(x=0, y=-4, text="My text", pen="0.5p,darkgreen", clearance="+tO")

fig.show()


# %%
# Plotting text with individual configurations
# --------------------------------------------
#
# To add text with individual ``font``, ``angle``, and ``justify`` one can
# provide lists with the corresponding arguments.

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
# Use an external txt file
# ------------------------
#
# It is also possible to add text labels via an external text file containing
# ``x``, ``y``, and ``text`` columns. Addionaly, columns to set the ``angle``,
# ``front``, and ``justify`` parameters can be provided. Here we give a
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
# The position parameter
# ----------------------
#
# Instead of using ``x`` and ``y``, the ``position`` parameter can be
# specified to set the reference point for the text on the plot.
# As for the ``justify`` parameter, the ``position`` parameter is specified
# by a two-letter (order independent) code, chosen from:
#
# * Vertical anchor: **T**\(op), **M**\(iddle), **B**\(ottom)
# * Horizontal anchor: **L**\(eft), **C**\(entre), **R**\(ight)
#
# This can be helpful to add text labels to subplot or text labels out of
# the map frame, e.g., for depth slices.

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -5, 5], projection="X5c", frame=["WStr", "af"])

fig.text(
    text="(a)",
    position="TL",
    offset="0.1c/-0.1c",
    justify="TL",
)

# -----------------------------------------------------------------------------
fig.shift_origin(xshift="+w1c")

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
    text="@@100 km",
    position="TC",
    justify="MC",
    offset="0c/0.2c",
    no_clip=True,
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
