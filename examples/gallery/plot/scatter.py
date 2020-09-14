"""
Scatter plots with a legend
---------------------------

TODO: Add more docstrings.

Modified from the matplotlib example: https://matplotlib.org/gallery/lines_bars_and_markers/scatter_with_legend.html
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
for color in ["blue", "orange", "green"]:
    x, y = np.random.rand(2, n)  # random X and Y data in [0,1]
    sizes = np.random.rand(n) * 0.5  # random size, in cm
    # plot data points as circles ('c'), with different sizes
    fig.plot(x, y, style="c", sizes=sizes, color=color, label=f"{color}+S0.25c", t=70)

fig.legend(t=30)
fig.show()
