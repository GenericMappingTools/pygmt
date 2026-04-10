"""
Area between curves
-------------------
Using the ``fill_between`` parameter of the :meth:`pygmt.Figure.plot` method it is
possible to fill the area between two curves y1 and y2. Different fills (colors or
patterns) can be used for the areas y1 > y2 and y1 < y2. Optionally, the curves can
be drawn.
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

data_df = pd.DataFrame({"x": x, "y1": y1, "y2": y2})
# -----------------------------------------------------------------------------
# Set up new Figure instance
fig = gmt.Figure()
fig.basemap(region=[-10, 10, -5, 5], projection="X15c/5c", frame=True)

fig.plot(
    data=data_df,
    fill="orange",
    fill_between="c+gsteelblue+lshort < long",
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
    fill_between="c+gp17+p1p,black,dashed",
)

fig.show()

# sphinx_gallery_thumbnail_number = 1
