r"""
Cartesian logarithmic
=====================

**X**\ *width*\ [**l**][/*height*\ [**l**]] or
**x**\ *x-scale*\ [**l**][/*y-scale*\ [**l**]]

Give the *width* of the figure and the optional *height*.
The lower-case version **x** is similar to **X** but expects
an *x-scale* and an optional *y-scale*.
Each axis with a logarithmic transformation requires **l** after
its size argument.
"""

# %%
import numpy as np
import pygmt

# Create a list of x-values 0-100
xline = np.arange(0, 101)
# Create a list of y-values that are the square root of the x-values
yline = xline**0.5
# Create a list of x-values for every 10 in 0-100
xpoints = np.arange(0, 101, 10)
# Create a list of y-values that are the square root of the x-values
ypoints = xpoints**0.5

fig = pygmt.Figure()
fig.basemap(
    region=[1, 100, 0, 10],
    # Set a logarithmic transformation on the x-axis
    projection="X15cl/10c",
    # Set the figures frame and color as well as
    # annotations, ticks, and gridlines
    frame=["WSne+gbisque", "xa2g3", "ya2f1g2"],
)

# Set the line thickness to "2p", the color to "black", and the style to "dashed"
fig.plot(x=xline, y=yline, pen="2p,black,dashed")

# Plot the square root values on top of the line
# Use squares with a size of 0.3 centimeters, an "orange" fill and a "black" outline
# Symbols are not clipped if they go off the figure
fig.plot(x=xpoints, y=ypoints, style="s0.3c", fill="orange", pen="black", no_clip=True)
fig.show()
