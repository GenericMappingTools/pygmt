r"""
Cartesian linear
================

**X**\ *width*/[*height*]: Give the *width* of the figure and the optional
*height*.
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
