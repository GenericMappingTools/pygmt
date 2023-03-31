r"""
Cartesian logarithmic
=====================

**X**\ *width*\ [**l**]/[*height*\ [**l**]]: Give the *width* of the figure and
the optional *height*. Each axis with a logarithmic transformation
requires **l** after its size argument.
"""
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
fig.plot(
    region=[1, 100, 0, 10],
    # Set a logarithmic transformation on the x-axis
    projection="X15cl/10c",
    # Set the figures frame and color as well as
    # annotations, ticks, and gridlines
    frame=["WSne+gbisque", "xa2g3", "ya2f1g2"],
    x=xline,
    y=yline,
    # Set the line thickness to "1p", the color to "blue",
    # and the style to "-", i.e. "dashed"
    pen="1p,blue,-",
)
# Plot square root values as points on the line
# Style of points is 0.3 cm squares, color fill is "red" with a "black" outline
# Points are not clipped if they go off the figure
fig.plot(x=xpoints, y=ypoints, style="s0.3c", fill="red", no_clip=True, pen="black")
fig.show()
