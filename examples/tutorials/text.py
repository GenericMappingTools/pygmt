"""
Plotting text
=============

It is often useful to add annotations to a map plot. This is handled by
:meth:`pygmt.Figure.text`.
"""

import pygmt

########################################################################################
# Basic map annotation
# --------------------
#
# Text annotations can be added to a map using the :meth:`text` method of the
# :class:`pygmt.Figure`.
#
# Full details of the GMT6 command `text` can be found `here<https://docs.generic-mapping-tools.org/latest/text.html>`_.
# The Python binding to this command is documented `here<https://www.pygmt.org/latest/api/generated/pygmt.Figure.text.html>`_.
#
# Here we create a simple map and add an annotation using the ``text``, ``x``,
# and ``y`` arguments to specify the annotation text and position in the
# projection frame. ``text``, ``x``, and ``y`` accept `int`, `str`, or `float`.

fig = pygmt.Figure()
with pygmt.config(MAP_FRAME_TYPE="plain"):
    fig.basemap(region=[108, 120, -5, 8], projection="M20c", frame="a")
fig.coast(land="black", water="skyblue")

# Plotting text annotations using single elements
fig.text(text="SOUTH CHINA SEA", x=112, y=6)

# Plotting text annotations using lists of elements
fig.text(text=["CELEBES SEA", "JAVA SEA"], x=[119, 112], y=[3.25, -4.6])

fig.show()

########################################################################################
# Changing font style
# -------------------
# The size, family/weight, and colour of an annotation can be specified using the ``font`` argument.
#
# A list of all recognised fonts can be found `here<https://docs.generic-mapping-tools.org/latest/cookbook/postscript_fonts.html>`_),
# including details of how to use non-default fonts.

fig = pygmt.Figure()
with pygmt.config(MAP_FRAME_TYPE="plain"):
    fig.basemap(region=[108, 120, -5, 8], projection="M20c", frame="a")
fig.coast(land="black", water="skyblue")

# Customising the font style
fig.text(text="BORNEO", x=114.0, y=0.5, font="22p,Helvetica-Bold,white")

fig.show()

########################################################################################
# Plotting from a text file
# -------------------------
#
# It is also possible to add annotations from a file containing `x`, `y`, and
# `text` fields. Here we give a complete example.

fig = pygmt.Figure()
with pygmt.config(MAP_FRAME_TYPE="plain"):
    fig.basemap(region=[108, 120, -5, 8], projection="M20c", frame="a")
fig.coast(land="black", water="skyblue")

# Plot region names / sea names
fig.text(textfiles="examples.txt", font="22p,Helvetica-Bold,white")

# Plot names of seas
fig.text(text=["CELEBES SEA", "JAVA SEA"], x=[119, 112], y=[3.25, -4.6])
fig.text(text="SULU SEA", x=119.12, y=7.25, angle=-40)
fig.text(text="SOUTH CHINA SEA", x=112, y=6, angle=40)
fig.text(text="MAKASSAR STRAIT", x=118.4, y=-1, angle=65)
fig.show()

########################################################################################
# ``justify`` argument
# --------------------
#
# ``justify`` is used to define the anchor point for the bounding box for text
# being added to a plot. The following code segment demonstrates the
# positioning of the anchor point relative to the text.
#
# The anchor is specified with a two letter (order independent) code, chosen
# from:
# * Horizontal anchor: L(eft), C(entre), R(ight)
# * Vertical anchor: T(op), M(iddle), B(ottom)

fig = pygmt.Figure()
fig.basemap(region=[0, 4, 0, 4], projection="X10c", frame="WSen")
for i, y_justify in enumerate(["T", "M", "B"]):
    y_pos = 3.5 - i * 1.5
    fig.plot(x=[0.0, 4.0], y=[y_pos, y_pos], pen="3p,red@85")
    for j, x_justify in enumerate(["L", "C", "R"]):
        justify_text = x_justify + y_justify
        x_pos = 0.5 + j * 1.5
        fig.text(
            text=justify_text,
            x=x_pos,
            y=y_pos,
            font="28p,Helvetica-Bold,black",
            justify=justify_text,
        )
        fig.plot(x=[x_pos, x_pos], y=[0.0, 4.0], pen="3p,red@85")
fig.show()

########################################################################################
# ``angle`` argument
# ------------------
# ``angle`` is an optional argument used to specify the clockwise rotation of
# the text from the horizontal.

fig = pygmt.Figure()
fig.basemap(region=[0, 4, 0, 4], projection="X10c", frame="WSen")
for i in range(0, 360, 30):
    fig.text(text=f"`          {i} Degrees", x=2, y=2, justify="LM", angle=i)
fig.show()

########################################################################################
# Additional arguments
# --------------------
#
# Text can be further configured by passing an argument corresponding to the
# flag names in GMT, following the same convention as described in the GMT
# documentation. It is hoped that over time more bindings to these arguments
# will be written into PyGMT.

fig = pygmt.Figure()
fig.basemap(region=[0, 1, 0, 1], projection="X5c", frame="WSen")
fig.text(text="Green", x=0.5, y=0.5, G="green")
fig.show()
