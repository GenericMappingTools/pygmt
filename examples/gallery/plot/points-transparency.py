"""
Points with varying transparency
--------------------------------

Plotting points with varying transparency is simply passing an array to the
``transparency`` argument.
"""

import numpy as np
import pygmt

# prepare the input x and y data
x = np.linspace(0, 3.0 * np.pi, 100)
y = np.sin(x)
# transparency level in percentage from 0 (i.e., opaque) to 100
transparency = np.linspace(0, 100, x.size)

fig = pygmt.Figure()
fig.basemap(
    region=[x.min(), x.max(), y.min() * 1.1, y.max() * 1.1],
    frame=["af", 'WSrt+t"Varying Transparency"'],
    projection="X10c/6c",
)
fig.plot(x=x, y=y, style="c0.15c", color="blue", transparency=transparency)
fig.show()
