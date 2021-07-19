"""
Contours
--------
The :meth:`pygmt.Figure.contour` method can plot contour lines from a table of points by direct triangulation.
The data to the triangulation can be provided in one of three options:

#. ``x``, ``y``, ``z`` 1d :class:`numpy.ndarray` data columns.
#. ``data`` 2d :class:`numpy.ndarray` data matrix with 3 columns corresponding
   to ``x``, ``y``, ``z``.
#. ``data`` path string to a file containing the ``x``, ``y``, ``z`` in a
   tabular format.

The parameters ``levels`` and ``annotation`` are deciding on the contours intervals and intervals of the
annotation on the contours respectively.

In this example we supply the data as  1d :class:`numpy.ndarray` with the ``x``, ``y``,
and ``z`` parameters and draw the contours using a 0.5p pen with contours every 10 ``z`` values and
annotations every 20 ``z`` values.
"""


import numpy as np
import pygmt

# building the contours underling data with the function z = x^2 + y^2
X, Y = np.meshgrid(np.linspace(-10, 10, 50), np.linspace(-10, 10, 50))
Z = X ** 2 + Y ** 2
x, y, z = X.flatten(), Y.flatten(), Z.flatten()


fig = pygmt.Figure()
fig.contour(
    region=[-10, 10, -10, 10],
    projection="X10c/10c",
    frame="ag",
    pen="0.5p",
    # passing the data as 3 1d data columns
    x=x,
    y=y,
    z=z,
    # set the contours z values intervals to 5
    levels=5,
    # set the contours annotation intervals to 20
    annotation=20,
)
fig.show()
