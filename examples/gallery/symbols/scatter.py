"""
Scatter plots with a legend
---------------------------

To create a scatter plot with a legend one may use a loop and create one
scatter plot per item to appear in the legend and set the label accordingly.

Modified from the matplotlib example:
https://matplotlib.org/stable/gallery/lines_bars_and_markers/scatter_with_legend.html
"""

import numpy as np
import pygmt

np.random.seed(19680801)
n = 200  # number of random data points

fig = pygmt.Figure()
fig.basemap(
    region=[-0.1, 1.1, -0.1, 1.1],
    projection="X10c/10c",
    frame=["xa0.2fg", "ya0.2fg", "WSrt"],
)
for fill in ["gray73", "darkorange", "slateblue"]:
    x, y = np.random.rand(2, n)  # random X and Y data in [0,1]
    size = np.random.rand(n) * 0.5  # random size [0,0.5], in cm
    # plot data points as circles (style="c"), with different sizes
    fig.plot(
        x=x,
        y=y,
        style="c",
        size=size,
        fill=fill,
        # Set the legend label,
        # and set the symbol size to be 0.25 cm (+S0.25c) in legend
        label=f"{fill}+S0.25c",
        transparency=50,  # set transparency level for all symbols
    )

fig.legend(transparency=30)  # set transparency level for legends
fig.show()
