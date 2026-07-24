"""
Ternary diagram
===============

The :meth:`pygmt.Figure.ternary` method can draw ternary diagrams. The example
shows how to plot circles with a diameter of 0.1 centimeters
(``style="c0.1c"``) on a 10-centimeters-wide (``width="10c"``) ternary diagram
at the positions listed in the first three columns of the sample dataset
``rock_compositions``, with default annotations and gridline spacings, using
the specified labeling defined via ``alabel``, ``blabel``, and ``clabel``.
Points are colored based on the values given in the fourth column of the
sample dataset via ``cmap=True``.
"""

# %%
import pygmt
from pygmt.params import Axis, Frame, Position

fig = pygmt.Figure()

# Load sample data
data = pygmt.datasets.load_sample_data(name="rock_compositions")

# Define a colormap to be used for the values given in the fourth column
# of the input dataset
pygmt.makecpt(cmap="SCM/batlow", series=[0, 80, 10])

fig.ternary(
    data,
    region=[0, 100, 0, 100, 0, 100],
    width="10c",
    style="c0.1c",
    alabel="Limestone",
    blabel="Water",
    clabel="Air",
    cmap=True,
    frame=Frame(
        xaxis=Axis(
            annot=True, tick=True, grid=True, label="Limestone component", unit="%"
        ),
        yaxis=Axis(annot=True, tick=True, grid=True, label="Water component", unit="%"),
        zaxis=Axis(annot=True, tick=True, grid=True, label="Air component", unit="%"),
    ),
)

# Add a colorbar indicating the values given in the fourth column of the input dataset
fig.colorbar(
    position=Position("BC", cstype="outside", offset=(0, 1.5)), label="Permittivity"
)
fig.show()
