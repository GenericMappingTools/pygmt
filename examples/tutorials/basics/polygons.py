"""
Plotting polygon
================

Plotting plotting is handled by :meth:`pygmt.Figure.plot`.
refere to choropleth map for geopandas polygon geometry.
"""

# %%
import pygmt

# %%
# Plot polygons
# -------------

x_list = [-2, 1, 3, 0, -4, -2]
y_list = [-3, -1, 1, 3, 2, -3]

# %%
# text

fig = pygmt.Figure()
fig.basemap(region=[-5, 5] * 2, projection="X5c", frame=True)

fig.plot(x=x_list, y=y_list)

fig.show()

# %%
# text

fig = pygmt.Figure()
fig.basemap(region=[-5, 5] * 2, projection="X5c", frame=True)

fig.plot(x=x_list, y=y_list, pen="2p,darkred,dashed")

fig.show()

# %%
# text
fig = pygmt.Figure()
fig.basemap(region=[-5, 5] * 2, projection="X5c", frame=True)

fig.plot(x=x_list, y=y_list, fill="orange", pen="2p,darkred,dashed")

fig.show()


# %%
# Close polygons
# --------------

x_list = [-2, 1, 3, 0, -4]
y_list = [-3, -1, 1, 3, 2]

# %%
# text
fig = pygmt.Figure()
fig.basemap(region=[-5, 5] * 2, projection="X5c", frame=True)

fig.plot(x=x_list, y=y_list, pen=True)

fig.shift_origin(xshift="+w1c")
fig.basemap(region=[-5, 5] * 2, projection="X5c", frame=True)

fig.plot(x=x_list, y=y_list, pen=True, close=True)

fig.show()

# %%
# text
fig = pygmt.Figure()
fig.basemap(region=[-5, 5] * 2, projection="X5c", frame=True)

fig.plot(x=x_list, y=y_list, pen=True)

fig.shift_origin(xshift="+w1c")
fig.basemap(region=[-5, 5] * 2, projection="X5c", frame=True)

fig.plot(x=x_list, y=y_list, pen=True, fill="orange")

fig.show()

# sphinx_gallery_thumbnail_number = 3
