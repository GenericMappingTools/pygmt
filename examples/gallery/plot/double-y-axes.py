"""
Double Y-axes
-------------

The ``frame`` parameter of the plotting methods of the :class:`pygmt.Figure`
class can control which axes should be plotted and possibly show annotations
and tick marks. By default, all 4 axes are plotted, along with annotations
and tick marks (denoted **W**, **S**, **E**, **N**). Lower case versions (**w**, **s**,
**e**, **n**) can be used to denote to only plot the axes with tick marks. We
can also only plot the axes without annotations and tick marks using **l**
(left axis), **r** (right axis), **t** (top axis), **b** (bottom axis).
"""

import numpy as np
import pygmt

# Generate common x values and two kinds of y values
x = np.linspace(1.0, 9.0, num=9)
y1 = x
y2 = x ** 2 + 110

fig = pygmt.Figure()

# Plot y1
# The bottom axis (S) is plotted with annotations and tick marks
# The top axis (t) is plotted without annotations and tick marks
fig.basemap(region=[0, 10, 0, 10], projection="X15c/15c", frame=["St", "xaf+lx"])
# The left axis (W) is plotted with customed annotations, tick marks and labels
with pygmt.config(
    MAP_FRAME_PEN="1.5p,blue",
    MAP_TICK_PEN="0.5p,blue",
    FONT_ANNOT_PRIMARY="12p,Helvetica,blue",
    FONT_LABEL="16p,Helvetica,blue",
):
    fig.basemap(frame=["W", "yaf+ly1"])

# Plot the line for y1
fig.plot(x=x, y=y1, pen="1p,blue")
# Plot points for y1
fig.plot(x=x, y=y1, style="c0.2c", color="blue", label="y1")

# Plot y2
# The right axis (E) is plotted with customed annotations, tick marks, and labels
with pygmt.config(
    MAP_FRAME_PEN="1.5p,red",
    MAP_TICK_PEN="0.5p,red",
    FONT_ANNOT_PRIMARY="12p,Helvetica,red",
    FONT_LABEL="16p,Helvetica,red",
):
    fig.basemap(region=[0, 10, 100, 200], frame=["E", "yaf+ly2"])
# Plot the line for y2
fig.plot(x=x, y=y2, pen="1p,red")
# Plot points for y2
fig.plot(x=x, y=y2, style="s0.28c", color="red", label="y2")

fig.legend(position="JTL+jTL+o0.1c", box=True)

fig.show()
