"""
Legend
======

The :meth:`pygmt.Figure.legend` method can automatically create a legend for
symbols plotted using :meth:`pygmt.Figure.plot`. A legend entry is only added
when the ``label`` parameter is used to state the desired text. Optionally,
to adjust the legend, users can append different modifiers. A list of all
available modifiers can be found at :gmt-docs:`gmt.html#l-full`. To create a
multiple-column legend **+N** is used with the desired number of columns.
For more complicated legends, users may want to write an ASCII file with
instructions for the layout of the legend items and pass it to the ``spec``
parameter of :meth:`pygmt.Figure.legend`. For details on how to set up such a
file, please see the GMT documentation at :gmt-docs:`legend.html#legend-codes`.
In this example the same plot is created twice, first with a vertical (default)
and then with a horizontal legend.
"""

# %%
import numpy as np
import pygmt

# Set up some test data
x = np.arange(-10, 10, 0.1)
y1 = np.sin(x)
y2 = np.cos(x)


# Create new Figure() object
fig = pygmt.Figure()

# -----------------------------------------------------------------------------
# Left: Vertical legend (one column, default)
fig.basemap(projection="X10c", region=[-10, 10, -1.5, 1.5], frame=True)

# Use the label parameter to state to text label for the legend entry
fig.plot(x=x, y=y1, pen="1p,green3", label="Sine")

fig.plot(x=x, y=y2, style="c0.1c", fill="dodgerblue", label="Cosine")

# Add a legend to the plot; place it within the plot bounding box at position
# ("J") TopRight with a anchor point ("j") TopRight and an offset of 0.2
# centimeters in x and y directions; surround the legend with a box
fig.legend(position="JTR+jTR+o0.2c", box=True)

fig.shift_origin(xshift="+w1c")

# -----------------------------------------------------------------------------
# Right: Horizontal legend (here two columns)
fig.basemap(projection="X10c", region=[-10, 10, -1.5, 1.5], frame=["wStr", "af"])

# +N sets the number of columns corresponding to the given number, here two
fig.plot(x=x, y=y1, pen="1p,green3", label="Sine+N2")

fig.plot(x=x, y=y2, style="c0.1c", fill="dodgerblue", label="Cosine")

# For multi-column legends users have to provide the width via +w, here it is
# set to 4.5 centimeters
fig.legend(position="JTR+jTR+o0.2c+w4.5c", box=True)

fig.show()
