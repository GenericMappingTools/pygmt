"""
Scatter plot with histograms
----------------------------
To create a scatter plot with histograms at the sides of the plot one
can use :meth:`pygmt.Figure.plot` in combination with
:meth:`pygmt.Figure.histogram`.
"""

import numpy as np
import pygmt

np.random.seed(19680801)

# generate random data
x = np.random.randn(1000)
y = np.random.randn(1000)

# get axis limits
xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))

fig = pygmt.Figure()
fig.basemap(
    region=[-xymax - 0.5, xymax + 0.5, -xymax - 0.5, xymax + 0.5],
    projection="X10c/10c",
    frame=["WSrt", "a1"],
)

fillcol = "seagreen"

# plot data points as circles with a diameter of 0.25 centimeters
fig.plot(x=x, y=y, style="c0.25c", fill=fillcol, transparency=50)

# shift the plot origin and add top margin histogram
fig.shift_origin(yshift="10.25c")

fig.histogram(
    projection="X10c/2c",
    frame=["Wsrt", "y+lCounts"],
    # Since no y-range is specified, ymax is calculated automatically
    region=[-xymax - 0.5, xymax + 0.5, 0, 0],
    data=x,
    fill=fillcol,
    histtype=0,
    series=0.1,
)

# shift the plot origin and add right margin histogram
fig.shift_origin(yshift="-10.25c", xshift="10.25c")

fig.histogram(
    horizontal=True,
    projection="X2c/10c",
    # Note that x and y are flipped here due to horizontal=True
    frame=["wSrt", "y+lCounts"],
    region=[-xymax - 0.5, xymax + 0.5, 0, 0],
    data=y,
    fill=fillcol,
    histtype=0,
    series=0.1,
)

fig.show()
