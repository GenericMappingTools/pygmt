"""
Quoted lines
------------
GMT allows to plot lines with text, so-called *quoted lines*.
Such lines can be achieved by passing ``"q"`` to the ``style``
parameter of :meth:`pygmt.Figure.plot`. This example shows how
the display of the text can be adjusted. To modify the base
line via the ``pen`` parameter, you may want to have a look at
the :doc:`Line styles example </gallery/lines/linestyles>`.
"""

import numpy as np
import pygmt

# Generate a two-point line for plotting
x = np.array([1, 4])
y = np.array([20, 20])

fig = pygmt.Figure()
fig.basemap(
    region=[0, 10, 0, 20],
    projection="X15c/15c",
    frame="+tQuoted Lines",
)

# Plot different quoted lines
for quotedline in [
    # xxx
    "qd1c:+ltext",
    # xxx
    "qd1.5c:+ltext",
    # xxx
    "qd1c:+ltext+i",
    # xxx
    "qn5:+ltext",
    # xxx
    "qN5:+ltext",
    # xxx
    "qN-1:+ltext",
    # xxx
    "qN+1:+ltext",
    # xxx
    "qd1c:+ltext+jTC",
    # xxx
    "qd1c:+ltext+jBR",
    # xxx
    "qd1c:+ltext+a20",
    # xxx
    "qd1c:+ltext+f13p",
    # xxx
    "qd1c:+ltext+fCourier-Bold",
    # xxx
    "qd1c:+ltext+fred",
    # xxx
    "qd1c:+ltext+p0.5p,blue",
    # xxx
    "qd1c:+ltext+p0.5p,blue+o",
    # xxx
    "qd1c:+ltext+p0.5p,blue+o+c0.1c/0.1c",
    # xxx
    "qd1c:+ltext+gdodgerblue",
]:
    y -= 1  # Move current line down
    fig.plot(x=x, y=y, pen="1.25p", style=quotedline)
    fig.text(
        x=x[-1],
        y=y[-1],
        text=quotedline,
        font="Courier-Bold",
        justify="ML",
        offset="0.75c/0c",
    )

fig.show()


###############################################################################
# For curved text following the line, append ``"+v"``.

# Generate sinus curve
x = np.arange(0, 10 * np.pi, 0.1)
y = np.sin(0.8 * x)

fig = pygmt.Figure()

fig.basemap(
    region=[0, 30, -4, 4],
    projection="X10c/5c",
    frame=True,
)

fig.plot(
    x=x,
    y=y + 2,
    style="qd1.2c:+lstraight text+f5p",
    pen="1p,blue",
)

fig.plot(
    x=x,
    y=y - 2,
    style="qd1.2c:+lcurved text+f5p+v",
    pen="1p,blue",
)

fig.show()
