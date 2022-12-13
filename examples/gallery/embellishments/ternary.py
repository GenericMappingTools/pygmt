"""
Ternary diagram
---------------

To plot circles (diameter = 0.1 cm) on a 10-centimeter-wide ternary diagram at the
positions listed in the sample dataset `rock_compositions`, with default annotations and
gridline spacings, using the specified labeling.
"""

import pygmt

fig = pygmt.Figure()

data = pygmt.datasets.load_sample_data(name="rock_compositions")

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
        "+givory",
    ],
)

fig.show()
