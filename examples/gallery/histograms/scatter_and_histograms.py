"""
Scatter plot with histograms
============================

To create a scatter plot with histograms at the sides of the plot one can use
:meth:`pygmt.Figure.plot` in combination with :meth:`pygmt.Figure.histogram`.
The positions of the histograms are plotted by offsetting them from the main scatter
plot using :meth:`pygmt.Figure.shift_origin`.
"""

# %%
import numpy as np
import pygmt

# Generate random x, y coordinates from a standard normal distribution.
# x are centered on 0 with a standard deviation of 1, and y are centered on 30 with a
# standard deviation of 2.
rng = np.random.default_rng()
x = rng.normal(loc=0, scale=1, size=1000)
y = rng.normal(loc=30, scale=2, size=1000)

# Get axis limits from the data limits. Extend the limits by 0.5 to add some margin.
xmin = np.floor(x.min()) - 0.5
xmax = np.ceil(x.max()) + 0.5
ymin = np.floor(y.min()) - 0.5
ymax = np.ceil(y.max()) + 0.5

# Set fill color for symbols and bars
fill = "seagreen"

# Set plot size.
# The scatter plot is 10x10, and the histograms are 10x3 and 3x10, respectively.
width, height = 10, 3

fig = pygmt.Figure()
fig.basemap(
    region=[xmin, xmax, ymin, ymax],
    projection=f"X{width}/{width}",
    frame=["WSrt", "xaf", "yaf"],
)

# Plot data points as circles with a diameter of 0.15 centimeters
fig.plot(x=x, y=y, style="c0.15c", fill=fill, transparency=50)

# Shift the plot origin and add top margin histogram
fig.shift_origin(yshift=width + 0.25)

fig.histogram(
    projection=f"X{width}/{height}",
    frame=["Wsrt", "xaf", "yaf+lCounts"],
    # Give the same value for ymin and ymax to have them calculated automatically.
    region=[xmin, xmax, 0, 0],
    data=x,
    fill=fill,
    pen="0.1p,white",
    histtype=0,
    series=0.2,
)

# Shift the plot origin and add right margin histogram
fig.shift_origin(yshift=-width - 0.25, xshift=width + 0.25)

fig.histogram(
    horizontal=True,
    projection=f"X{height}/{width}",
    # Note that the y-axis annotations, ticks, and label "Counts" are shown in x-axis
    # direction due to the rotation caused by horizontal=True
    frame=["wSrt", "xf", "y+lCounts"],
    region=[ymin, ymax, 0, 0],
    data=y,
    fill=fill,
    pen="0.1p,white",
    histtype=0,
    series=0.2,
)
fig.show()
