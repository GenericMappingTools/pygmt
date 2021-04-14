"""
Wiggle along tracks
--------------------

The :meth:`pygmt.Figure.wiggle` method can plot z = f(x,y) anomalies along
tracks. ``x``, ``y``, ``z`` can be specified as 1d arrays or within a specified
file.
"""

import numpy as np
import pygmt

# Create (x, y, z) triplets
x = np.arange(-7, 7, 0.1)
y = np.zeros(x.size)
z = 50 * np.exp(-((x / 3) ** 2)) * np.cos(2 * np.pi * x)

fig = pygmt.Figure()
fig.basemap(region=[-8, 12, -1, 1], projection="X10c", frame=["Snlr", "xa2f1"])
fig.wiggle(
    x=x,
    y=y,
    z=z,
    scale="20c",
    color=["red+p", "gray+n"],
    pen="1.0p",
    track="0.5p",
    position="jRM+w100+lnT",
)
fig.show()
