"""
Fill area between curves
========================
Using the ``fill_between`` parameter of the :meth:`pygmt.Figure.plot` method it is
possible to fill the area between two curves y1 and y2. Different fills (colors or
patterns) can be used for the areas y1 > y2 and y1 < y2. Optionally, the curves can be
drawn.
To plot an anomaly along a track use :meth:`pygmt.Figure.wiggle` and see the gallery
example :doc:`Wiggle along tracks </gallery/lines/wiggle>`.
"""

# %%
import numpy as np
import pandas as pd
import pygmt

# Generate some test data and create a pandas DataFrame
x = np.arange(-10, 10.2, 0.1)
y1 = np.sin(x * 3)
y2 = np.sin(x / 2)

data_df = pd.DataFrame({"x": x, "y1": y1, "y2": y2})


# %%
# Fill the areas between the two curves using the ``fill_between`` parameter. Use the
# ``fill`` parameter and the modifier **+g** for ``fill_between`` to set different fills
# for areas with y1 > y2 and y1 < y2, respectively. Use the ``label`` parameter and the
# modifier **+l** for ``fill_between`` to set the corresponding legend entries.

fig = pygmt.Figure()
fig.basemap(region=[-10, 10, -5, 5], projection="X15c/5c", frame=True)

fig.plot(
    data=data_df,
    fill="orange",
    label="short > long",
    fill_between="c+gsteelblue+lshort < long",
)

fig.legend()

fig.show()


# %%
# In addition to filling the areas, we can draw the curves. Use the ``pen`` parameter
# and the modifier **+p** for ``fill_between`` to set different lines for the two
# curves y1 and y2, respectively.

fig = pygmt.Figure()
fig.basemap(region=[-10, 10, -5, 5], projection="X15c/5c", frame=True)

fig.plot(
    data=data_df,
    fill="p8",
    pen="1p,black,solid",
    fill_between="c+gp17+p1p,black,dashed",
)

fig.show()


# %%
# To compare a curve y1 to a horizontal line, append **+y** to ``fill_between`` and give
# the desired y-level.

fig = pygmt.Figure()
fig.basemap(region=[-10, 10, -5, 5], projection="X15c/5c", frame=True)

fig.plot(
    data=data_df[["x", "y1"]],
    fill="p8",
    pen="1p,black,solid",
    # Define a horizontal line at y=0.42
    fill_between="c+gp17+p1p,black,dashed+y0.42",
)

fig.show()

# sphinx_gallery_thumbnail_number = 1
