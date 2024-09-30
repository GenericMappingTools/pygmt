r"""
Cartesian power
===============

**X**\ *width*\ [**p**\ *pvalue*][/*height*\ [**p**\ *pvalue*]] or
**x**\ *x-scale*\ [**p**\ *pvalue*][/*y-scale*\ [**p**\ *pvalue*]]

Give the *width* of the figure and the optional argument *height*.
The lower-case version **x** is similar to **X** but expects
an *x-scale* and an optional *y-scale*.
Each axis with a power transformation requires **p** and the exponent
for that axis after its size argument.
"""

# %%
import numpy as np
import pygmt

# Create a list of y-values 0-10
yvalues = np.arange(0, 11)
# Create a list of x-values that are the square of the y-values
xvalues = yvalues**2

fig = pygmt.Figure()
fig.basemap(
    region=[0, 100, 0, 10],
    # Set the power transformation of the x-axis, with a power of 0.5
    projection="X15cp0.5/10c",
    # Set the figures frame as well as annotations and ticks
    # The "p" forces to show only square numbers as annotations of the x-axis
    frame=["WSne+gbisque", "xfga1p", "ya2f1g"],
)

# Set the line thickness to "thick" (equals "1p", i.e. 1 point)
# Use as color "black" (default) and as style "solid" (default)
fig.plot(x=xvalues, y=yvalues, pen="thick,black,solid")

# Plot the data points on top of the line
# Use circles with 0.3 centimeters diameter, with an "orange" fill and a "black" outline
# Symbols are not clipped if they go off the figure
fig.plot(x=xvalues, y=yvalues, style="c0.3c", fill="orange", pen="black", no_clip=True)
fig.show()
