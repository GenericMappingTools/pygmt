"""
Area between curves
-------------------
Using the ``M`` parameter of the :meth:`pygmt.Figure.plot` method it is possible
to fill the area between two curves y_1 and y_2 with color. Different fills (colors
or patterns) can be used for the areas y_1 > y_2 and y_1 < y_2. Optionally, the
curves can be drawn.
"""

# %%
import numpy as np
import pandas as pd
import pygmt as gmt

# -----------------------------------------------------------------------------
# Generate some test data and create a pandas DataFrame
x = np.arange(-10, 10.2, 0.1)
y1 = np.sin(x * 3)
y2 = np.sin(x / 2)

data = np.array([x, y1, y2])
data_tp = data.transpose()

data_df = pd.DataFrame(data_tp, columns=["x", "y1", "y2"])

# -----------------------------------------------------------------------------
# Set up new Figure instance
fig = gmt.Figure()
fig.basemap(region=[-10, 10, -5, 5], projection="X15c/5c", frame=True)

fig.plot(
    data=data_df,
    fill="orange",
    M="c+gsteelblue+lshort < long",
    label="short > long",
)

fig.legend()

fig.show()


# %%
# Additionally we can draw the curves.

# Set up new Figure instance
fig = gmt.Figure()
fig.basemap(region=[-10, 10, -5, 5], projection="X15c/5c", frame=True)

fig.plot(
    data=data_df,
    fill="p8",
    pen="1p,black,solid",
    M="c+gp17+p1p,black,dashed",
)

fig.show()

# sphinx_gallery_thumbnail_number = 1
