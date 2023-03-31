"""
Color land and water
--------------------

The ``land`` and ``water`` parameters of :meth:`pygmt.Figure.coast` specify
a color to fill in the land and water masses, respectively. There are many
:gmt-docs:`color codes in GMT <gmtcolors.html>`, including standard GMT color
names (like ``"skyblue"``), R/G/B levels (like ``"0/0/255"``), a hex value
(like ``"#333333"``), and a gray level (like ``"gray50"``).
"""
import pygmt

fig = pygmt.Figure()
# Make a global Mollweide map with automatic ticks
fig.basemap(region="g", projection="W15c", frame=True)
# Plot the land as light gray, and the water as sky blue
fig.coast(land="#666666", water="skyblue")
fig.show()
