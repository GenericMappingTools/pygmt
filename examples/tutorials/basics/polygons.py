"""
Plotting polygons
=================

Plotting polygons is handled by the :meth:`pygmt.Figure.plot` method.

This tutorial focuses on input data given via lists or NumPy arrays. For
plotting GeoPandas polygon geometry, e.g. to create a chorophlet map, see
the gallery example https://www.pygmt.org/dev/gallery/maps/choropleth_map.html.
"""

# %%
import numpy as np
import pygmt

# %%
# Plot polygons
# -------------
#
# Set up sample data points as lists for the x and y values.

x_list = [-2, 1, 3, 0, -4, -2]
y_list = [-3, -1, 1, 3, 2, -3]

# %%
# Create a Cartesian plot via the :meth:`pygmt.Figure.basemap` method.
# Pass lists to the ``x`` and ``y`` parameters of the :meth:`pygmt.Figure.plot`
# method. Without further adjustments, lines are drawn between the data points.
# By default, the lines are 0.25-points thick, black, and solid. In this example,
# the data points are chosen to make the lines form a polygon.

fig = pygmt.Figure()
fig.basemap(region=[-5, 5] * 2, projection="X5c", frame=True)

fig.plot(x=x_list, y=y_list)

fig.show()

# %%
# The ``pen`` parameter can be used to adjust the lines or outline of the polygon.
# The argument passed to ``pen`` is one string with the comma-separated optional
# values *width*,\ *color*,\ *style*.

fig = pygmt.Figure()
fig.basemap(region=[-5, 5] * 2, projection="X5c", frame=True)

# Use a 2-points thick, darkred, dashed outline
fig.plot(x=x_list, y=y_list, pen="2p,darkred,dashed")

fig.show()

# %%
# Use the ``fill`` parameter to fill the polygon with a color or pattern.
# For the patterns avilable in GMT see the Technical Reference at
# https://www.pygmt.org/dev/techref/patterns.html.

fig = pygmt.Figure()
fig.basemap(region=[-5, 5] * 2, projection="X5c", frame=True)

# Fill the polygon with color "orange"
fig.plot(x=x_list, y=y_list, fill="orange", pen="2p,darkred,dashed")

fig.show()


# %%
# Close polygons
# --------------
#
# Set up sample data points as NumPy array for the x and y values. Now,
# the data points do not form a polygon.

x_array = np.array([-2, 1, 3, 0, -4])
y_array = np.array([-3, -1, 1, 3, 2])

# %%
# The ``close`` parameter can be used to force the polygon to be closed.

fig = pygmt.Figure()
fig.basemap(region=[-5, 5] * 2, projection="X5c", frame=True)

fig.plot(x=x_array, y=y_array, pen=True)

fig.shift_origin(xshift="+w1c")
fig.basemap(region=[-5, 5] * 2, projection="X5c", frame=True)

fig.plot(x=x_array, y=y_array, pen=True, close=True)

fig.show()

# %%
# When using the ``fill`` parameter, the polygon is automatically closed.

fig = pygmt.Figure()
fig.basemap(region=[-5, 5] * 2, projection="X5c", frame=True)

fig.plot(x=x_array, y=y_array, pen=True)

fig.shift_origin(xshift="+w1c")
fig.basemap(region=[-5, 5] * 2, projection="X5c", frame=True)

fig.plot(x=x_array, y=y_array, pen=True, fill="orange")

fig.show()

# sphinx_gallery_thumbnail_number = 3
