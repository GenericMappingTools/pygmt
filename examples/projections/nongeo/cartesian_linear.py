r"""
Cartesian linear
================

**X**\ *width*\ [/*height*] or **x**\ *x-scale*\ [/*y-scale*]

Give the *width* of the figure and the optional *height*.
The lower-case version **x** is similar to **X** but expects
an *x-scale* and an optional *y-scale*.

The Cartesian linear projection is primarily designed for regular
floating point data. To plot geographical data in a linear
projection, see the upstream GMT documentation
:gmt-docs:`Geographic coordinates
<cookbook/coordinate-transformations.html#geographic-coordinates>`.
To make the linear plot using calendar date/time as input
coordinates, see the GMT documentation
:gmt-docs:`Calendar time coordinates
<cookbook/coordinate-transformations.html#calendar-time-coordinates>`.
"""
import pygmt

fig = pygmt.Figure()
fig.plot(
    # The x and y parameters determine the coordinates of lines
    x=[3, 9, 2],
    y=[4, 9, 37],
    pen="3p,red",
    # The region parameter sets the x and y ranges of the
    # Cartesian projection
    region=[0, 10, 0, 50],
    projection="X15c/10c",
    # "WSne" is passed to the frame parameter to put annotations
    # only on the left and bottom axes
    frame=["af", "WSne"],
)
fig.show()
