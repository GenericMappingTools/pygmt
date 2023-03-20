"""
Histogram
---------
The :meth:`pygmt.Figure.histogram` method can plot regular histograms.
Using the ``series`` parameter allows to set the interval for the width of
each bar. The type of the histogram (frequency count or percentage) can be
selected via the ``histtype`` parameter. The ``fill`` of the
bars can be either a color or a pattern.
"""

import numpy as np
import pygmt

np.random.seed(100)

# Generate random elevation data from a normal distribution
mean = 100  # mean of distribution
stddev = 25  # standard deviation of distribution
data = mean + stddev * np.random.randn(521)

fig = pygmt.Figure()

with fig.subplot(
    nrows=1,
    ncols=2,
    figsize=("13.5c", "5c"),
    title="Histograms",
):
    with fig.set_panel(panel=0):
        fig.histogram(
            data=data,
            # Define the frame, add title and set background color to
            # "lightgray", add labels for x and y axes
            frame=["WSne+glightgray", "x+lElevation in m", "y+lCounts"],
            # Generate evenly spaced bins by increments of 5
            series=5,
            # Use "red3" as color fill for the bars
            fill="red3",
            # Use a pen thickness of 1 point to draw the outlines
            pen="1p",
            # Choose histogram type 0, i.e., counts [Default]
            histtype=0,
        )

    with fig.set_panel(panel=1):
        fig.histogram(
            data=data,
            frame=["wSne+glightgray", "x+lElevation in m"],
            series=5,
            # Use pattern (p) number 8 as fill for the bars
            # with "lightblue" as background color (+b) and
            # "black" as foreground color (+f)
            fill="p8+blightblue+fblack",
            pen="1p",
            histtype=0,
        )

fig.show()
