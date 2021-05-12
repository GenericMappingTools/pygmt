"""
Histogram
---------
The :meth:`pygmt.Figure.histogram` method can plot regular histograms.
"""

import pygmt

fig = pygmt.Figure()

fig.histogram(
    table="@v3206_06.txt",
    region=[-6000, 0, 0, 30],
    series=250,
    fill="red3",
    frame=[
        'WSne+t"Histograms"+glightgray',
        'x+l"Topography (m)"',
        'y+l"Frequency"+u" %"',
    ],
    pen="1p",
    type=1,
)

fig.show()
