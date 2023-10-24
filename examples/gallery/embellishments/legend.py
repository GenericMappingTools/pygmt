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
"""

# %%
import numpy as np
import pygmt

# Set up some test data
x = np.arange(-10, 10, 0.2)
y1 = np.sin(x) + 1.1
y2 = np.cos(x) + 1.1
y3 = np.sin(x / 2) - 1.1
y4 = np.cos(x / 2) - 1.1


# Create new Figure() object
fig = pygmt.Figure()

fig.basemap(
    projection="X10c/7c",
    region=[-10, 10, -3.5, 3.5],
    frame=["WSne", "xaf+lx", "ya1f0.5+ly"],
)

# -----------------------------------------------------------------------------
# Top: Vertical legend (one column, default)

# Use the label parameter to state to text label for the legend entry
fig.plot(x=x, y=y1, pen="1p,green3", label="Sine(x)")

fig.plot(x=x, y=y2, style="c0.07c", fill="dodgerblue", label="Cosine(x)")

# Add a legend to the plot; place it within the plot bounding box at position
# ("J") TopRight with a anchor point ("j") TopRight and an offset of 0.2
# centimeters in x and y directions; surround the legend with a box
fig.legend(position="JTR+jTR+o0.2c", box=True)


# -----------------------------------------------------------------------------
# Bottom: Horizontal legend (here two columns)

# +N sets the number of columns corresponding to the given number, here two
fig.plot(x=x, y=y3, pen="1p,darkred,-", label="Sine(x/2)+N2")

fig.plot(x=x, y=y4, style="s0.07c", fill="orange", label="Cosine(x/2)")

# For a multi-column legend, users have to provide the width via +w, here it
# is set to 5 centimeters; position and anchor point are set to BottomRight
fig.legend(position="JBR+jBR+o0.2c+w5c", box=True)


fig.show()
