"""
Histogram
---------
The :meth:`pygmt.Figure.histogram` method can plot regular histograms.
"""

import pygmt

fig = pygmt.Figure()

fig.histogram(
    table="@v3206_06.txt",
    # specify the "region" of interest [xmin, xmax, ymin, ymax]
    region=[-6000, 0, 0, 30],
    # generate evenly spaced bins by increments of 250
    series=250,
    # use red3 as color fill for the bars
    fill="red3",
    # define the frame, add title and set background color to
    # lightgray, add annotations for x and y axis
    frame=[
        'WSne+t"Histograms"+glightgray',
        'x+l"Topography (m)"',
        'y+l"Frequency"+u" %"',
    ],
    # use a pen size of 1p to draw the outlines
    pen="1p",
    # choose histogram type 1 = frequency_percent
    type=1,
)

fig.show()
