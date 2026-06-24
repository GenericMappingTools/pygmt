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
fig.basemap(region=[-10, 10, -5, 5], projection="X15c/5c", frame=True)

fig.fill_between(
    x=x, y=y1, y2=y2, fill="orange", fill2="steelblue", label="y1(x)", label2="y2(x)"
)
fig.legend()
fig.show()


# %%
# In addition to filling the areas, we can draw the curves. Use the ``pen`` and
# ``pen2`` parameters to set different lines for the two curves y1 and y2, respectively.

fig = pygmt.Figure()
fig.basemap(region=[-10, 10, -5, 5], projection="X15c/5c", frame=True)
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
fig.basemap(region=[-10, 10, -5, 5], projection="X15c/5c", frame=True)

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
# parameter ``x2``.

x1 = np.linspace(0, 4, 100)
y1 = np.sin(5 * x1)
x2 = np.array([0, 0.21, 0.4, 0.63, 0.89, 1.18, 1.45, 1.69, 1.96, 2.26, 2.61, 3.23, 3.49, 4.0])
y2 = 0.5 * np.cos(3 * x2)

fig = pygmt.Figure()
fig.basemap(region=[0, 4, -1.2, 1.2], projection="X10c/5c", frame=True)

fig.fill_between(
    x=x1,
    y=y1,
    x2=x2,
    y2=y2,
    fill="orange",
    fill2="steelblue",
    pen="1p,darkred",
    pen2="1p,darkblue",
    label="y1(x1)",
    label2="y2(x2)",
)

# Mark sampling points
fig.plot(x=x1, y=y1, style="c0.1c", fill="darkred")
fig.plot(x=x2, y=y2, style="c0.1c", fill="darkblue")

fig.legend()
fig.show()

# sphinx_gallery_thumbnail_number = 1
