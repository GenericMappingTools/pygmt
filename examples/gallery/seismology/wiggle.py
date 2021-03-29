"""
Wiggle along tracks
--------------------

The :meth:`pygmt.Figure.wiggle` method can plot z = f(x,y) anomalies along
tracks. ``x``, ``y``, ``z`` can be specified as 1d arrays or within a specified
file.
"""

import numpy as np
import pygmt

# Create (x, y, z) which is equal to the gmt math above
x = np.arange(-8, 7, 0.1)
y = np.zeros(x.size)
z = 50 * np.exp(-((x / 3) ** 2)) * np.cos(2 * np.pi * x)

fig = pygmt.Figure()
fig.basemap(
    region=[-10, 10, -1, 1], projection="X15c", frame=["WSne", "xa2f1", "ya0.5"]
)
fig.wiggle(
    x=x,
    y=y,
    z=z,
    scale="10c",
    position="jRM+w100+lnT",
    track="0.5p",
    color="red+p+n",
    pen="0.5p",
)
fig.show()
