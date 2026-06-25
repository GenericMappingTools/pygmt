"""
Fill area between curves
========================
The :meth:`pygmt.Figure.fill_between` method fills the area between two curves y1 and
y2. Different fills (colors or patterns) can be used for the areas y1 > y2 and
y1 < y2. Optionally, the curves can be drawn. The two curves can be co-registered or
have different x-coordinates.
To plot an anomaly along a track use :meth:`pygmt.Figure.wiggle` and see the gallery
example :doc:`Wiggle along tracks </gallery/lines/wiggle>`.
"""

# %%
import numpy as np
import pygmt

# Generate some test data
x = np.arange(-10, 10.2, 0.1)
y1 = np.sin(3 * x)
y2 = np.sin(x / 2)


# %%
# Fill the areas between the two curves. Use the ``fill`` and ``fill2`` parameters to
# set different fills for areas with y1 > y2 and y1 < y2, respectively. Use the
# ``label`` and ``label2`` parameters to set the corresponding legend entries.

fig = pygmt.Figure()
fig.basemap(region=[-10, 10, -3.5, 3.5], projection="X15c/5c", frame=True)

fig.fill_between(
    x=x, y=y1, y2=y2, fill="orange", fill2="steelblue", label="y1(x)", label2="y2(x)"
)
fig.legend()
fig.show()


# %%
# In addition to filling the areas, we can draw the curves. Use the ``pen`` and
# ``pen2`` parameters to set different lines for the two curves y1 and y2, respectively.

fig = pygmt.Figure()
fig.basemap(region=[-10, 10, -3.5, 3.5], projection="X15c/5c", frame=True)
fig.fill_between(
    x=x,
    y=y1,
    y2=y2,
    fill="p8",
    fill2="p17",
    pen="1p,black,solid",
    pen2="1p,black,dashed",
)
fig.show()


# %%
# To compare a curve y1 to a horizontal line, pass the desired y-level to ``y2``.

fig = pygmt.Figure()
fig.basemap(region=[-10, 10, -3.5, 3.5], projection="X15c/5c", frame=True)

fig.fill_between(
    x=x,
    y=y1,
    y2=0.42,
    fill="p8",
    fill2="p17",
    pen="1p,black,solid",
    pen2="1p,black,dashed",
)
fig.show()


# %%
# Now, we use two non-co-registered curves, e.g., the two curves have different
# x-coordinates. For providing the x-coordinates for the second curve, use
# parameter ``x2``.  Via the ``legend_pen`` parameter the appearence in the legend
# can be changed to draw the legend entries as colored lines (using the fill colors)
# instead of filled boxes.

x1 = np.arange(-10, 10.2, 0.2)
y1 = np.sin(3 * x1)
# Partly Segmentation fault problem (at least on Windows)
x2 = np.sort((np.random.rand(20) - 0.5) * 20)
# Line limit still applies
x2 = np.array([-10, -8.21, -7.4, -6.63, -5.89, -4.18, -3.45, -2.69, -1.96, 0.26, 1.61, 2.23, 3.49, 4.0, 5.28, 6.79, 7.12, 8.25, 9.13, 10])  # noqa: E501
y2 = np.sin(x2 / 2)

fig = pygmt.Figure()
fig.basemap(region=[-10, 10, -3.5, 3.5], projection="X15c/5c", frame=True)

fig.fill_between(
    x=x1,
    y=y1,
    x2=x2,
    y2=y2,
    fill="orange",
    fill2="steelblue",
    pen="1p,darkred,solid",
    pen2="1p,darkblue,solid",
    label="y1(x1)",
    label2="y2(x2)",
    legend_pen="5p",
)

# Mark sampling points
fig.plot(x=x1, y=y1, style="c0.1c", fill="pink")
fig.plot(x=x2, y=y2, style="c0.1c", fill="cyan")

fig.legend()
fig.show()

# sphinx_gallery_thumbnail_number = 1
