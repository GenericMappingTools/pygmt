"""
Ternary diagram
---------------
The pygmt.Figure.ternary method can draw ternary diagrams. The example shows
how to plot circles with a diameter of 0.1 centimeters (``style=0.1c``) on a
10-centimeter-wide (```width=10c``) ternary diagram at the positions listed
in the first three columns of the sample dataset `rock_compositions`, with
default annotations and gridline spacings, using the specified labeling
defined via ``alabel``, ``blabel`` and ``clabel``. Points are colored based
on the values given in the fourth columns of the sample dataset via
``cmap=True``.
"""

import pygmt

fig = pygmt.Figure()

# Load sample data
data = pygmt.datasets.load_sample_data(name="rock_compositions")

# Define a colormap to be used for the values given in the fourth column
# of the input dataset
pygmt.makecpt(cmap="batlow", series=[0, 80, 10])

fig.ternary(
    data,
    region=[0, 100, 0, 100, 0, 100],
    width="10c",
    style="c0.1c",
    alabel="Limestone",
    blabel="Water",
    clabel="Air",
    cmap=True,
    frame=[
        "aafg+lLimestone component+u %",
        "bafg+lWater component+u %",
        "cagf+lAir component+u %",
    ],
)

# Shift origin -1 centimeters in y direction to avoid overlap
# between ternary diagram and colorbar
fig.shift_origin(yshift="-1c")

# Add a colorbar indicating the values given in the fourth column of
# the input dataset
fig.colorbar(frame=["x+lPermittivity"])
fig.show()
