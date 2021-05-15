"""
Histogram
---------
The :meth:`pygmt.Figure.histogram` method can plot regular histograms.
"""

import numpy as np
import pygmt

np.random.seed(100)

# generate example topography data
mu = 100  # mean of distribution
sigma = 25  # standard deviation of distribution
data = mu + sigma * np.random.randn(521)

fig = pygmt.Figure()

fig.histogram(
    table=data,
    # generate evenly spaced bins by increments of 5
    series=5,
    # use red3 as color fill for the bars
    fill="red3",
    # define the frame, add title and set background color to
    # lightgray, add annotations for x and y axis
    frame=['WSne+t"Histogram"+glightgray', 'x+l"Topography (m)"', 'y+l"Counts"'],
    # use a pen size of 1p to draw the outlines
    pen="1p",
    # choose histogram type 0 = counts [default]
    histtype=0,
)

fig.show()
