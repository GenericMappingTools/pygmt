"""
Text formatting
===============

There are different options to format text added to a plot as well as labels of
colorbars, Cartesian axes and legend entries, including, superscripts, subscripts,
underlining and small caps (:doc:`Text Formatting </techref/text_formatting>`).
It's also possible to change the font as well as its color and size only for
specific characters of a longer text. The supported fonts are listed at
:doc:`Supported Fonts  </techref/fonts>`.
"""

# %%
import pygmt

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -5, 5], projection="X10c", frame=0)

# Change font color for specific characters
fig.text(x=0, y=3, text="@;63/124/173;P@;;@;255/212/59;y@;;@;238/86/52;GMT@;;")

# Change font size and style for a single character, respectively
fig.text(x=0, y=2, text="te@:15:x@::t     tex@%Courier-Oblique%t@%%")

# Superscript
fig.text(x=0, y=1, text="E = mc@+2@+")

# Subscripts and Greek letters
fig.text(x=0, y=0, text="@~s@~@-ij@- = c@-ijkl@- @~e@~@-ij@-")

# Combine two characters above each other
fig.text(x=0, y=-1, text="@!_~")

# Underline the text
fig.text(x=0, y=-2, text="@_underlined text@_")

# Use small caps
fig.text(x=0, y=-3, text="@#text in small caps@#")

fig.show()
