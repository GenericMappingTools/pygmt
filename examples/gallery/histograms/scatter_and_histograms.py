"""
Scatter plot with histograms
============================

To create a scatter plot with histograms at the sides of the plot one can use
:meth:`pygmt.Figure.plot` in combination with :meth:`pygmt.Figure.histogram`.
The positions of the histograms are plotte by offsetting them from the main
scatter plot using :meth:`pygmt.Figure.shift_origin`.
"""

# %%
import numpy as np
import pygmt

# Generate random data from a standard normal distribution centered on 0 with a
# standard deviation of 1
rng = np.random.default_rng(seed=19680801)
x = rng.normal(loc=0, scale=1, size=1000)
y = rng.normal(loc=0, scale=1, size=1000)

# Get axis limits
xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))

# Set plot width
fig_width = 10

# Set fill color for symbols and bars
fillcol = "seagreen"

fig = pygmt.Figure()
fig.basemap(
    region=[-xymax - 0.5, xymax + 0.5, -xymax - 0.5, xymax + 0.5],
    projection=f"X{fig_width}c/{fig_width}c",
    frame=["WSrt", "a1"],
)

# Plot data points as circles with a diameter of 0.15 centimeters
fig.plot(x=x, y=y, style="c0.15c", fill=fillcol, transparency=50)

# Shift the plot origin and add top margin histogram
fig.shift_origin(yshift=f"{fig_width + 0.25}c")

fig.histogram(
    projection=f"X{fig_width}c/2c",
    frame=["Wsrt", "xf1", "y+lCounts"],
    # Give the same value for ymin and ymax to have them calculated automatically
    region=[-xymax - 0.5, xymax + 0.5, 0, 0],
    data=x,
    fill=fillcol,
    pen="0.1p,white",
    histtype=0,
    series=0.1,
)

# Shift the plot origin and add right margin histogram
fig.shift_origin(yshift=f"-{fig_width + 0.25}c", xshift=f"{fig_width + 0.25}c")

fig.histogram(
    horizontal=True,
    projection=f"X2c/{fig_width}c",
    # Note that the y-axis annotation "Counts" is shown in x-axis direction due to the
    # rotation caused by horizontal=True
    frame=["wSrt", "xf1", "y+lCounts"],
    region=[-xymax - 0.5, xymax + 0.5, 0, 0],
    data=y,
    fill=fillcol,
    pen="0.1p,white",
    histtype=0,
    series=0.1,
)

fig.show()
