"""
Contours
--------
The :meth:`pygmt.Figure.contour` method can plot contour lines from a table of points.
"""


import numpy as np
import pygmt

X, Y = np.meshgrid(np.linspace(-10, 10, 50), np.linspace(-10, 10, 50))
Z = X**2 + Y**2
x, y, z = X.flatten(), Y.flatten(), Z.flatten()

fig = pygmt.Figure()
fig.contour(
    region=[-10, 10, -10, 10],
    projection="X10c/10c",
    frame="ag",
    x=x,
    y=y,
    z=z,
    pen=1
)
fig.show()