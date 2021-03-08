"""
Double Y-axes
-------------

The ``frame`` parameter of the plotting methods of the :class:`pygmt.Figure`
class can control which axes should be plotted and possibly show annotations
and tick marks. By default, all the 4 axes are plotted, along with annotations
and tick marks (denoted **W**, **S**, **E**, **N**). Lower cases (**w**, **s**,
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
# The left (W) and bottom (S) axes are plotted with annotations and tick marks
fig.basemap(
    region=[0, 10, 0, 10], projection="X5c/5c", frame=["WS", "xaf+lx", "yaf+ly1"]
)
# Plot the line for y1
fig.plot(x=x, y=y1, pen="1p,blue")
# Plot points for y1
fig.plot(x=x, y=y1, style="c0.2c", color="blue", label="y1")

# Plot y2
# The right axis (E) is plotted with annotations and tick marks
# The top axis (t) is plotting without annotations and tick marks
fig.basemap(region=[0, 10, 100, 200], frame=["Et", "yaf+ly2"])
# Plot the line for y2
fig.plot(x=x, y=y2, pen="1p,red")
# Plot points for y2
fig.plot(x=x, y=y2, style="s0.28c", color="red", label="y2")

fig.legend(position="JTL+jTL+o0.1c", box=True)

fig.show()
