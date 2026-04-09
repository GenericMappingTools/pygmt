"""
Create grid mask from polygons
==============================
:func:`pygmt.grdmask`.

:func:`pygmt.grdlandmask` and gallery example https://www.pygmt.org/latest/gallery/images/grdlandmask.html.
"""

# %%
import numpy as np
import pygmt

# Define a study region
region = [120, 135, 25, 40]

# Define two polygons, here triangels, use nan to separate the polygons
polygon = np.array(
    [
        [125, 30],
        [130, 30],
        [130, 35],
        [125, 30],
        [np.nan, np.nan],
        [122, 37],
        [128, 37],
        [128, 39],
        [122, 37],
    ],
)

# Download elevation grid
grid = pygmt.datasets.load_earth_relief(region=region, resolution="30s")

# Create a grid mask based on the two polygons defined above, set all values
# outside the polygons to NaN
mask = pygmt.grdmask(region=region, data=polygon, spacing="30s", outside="NaN")

# Apply the grid mask to the downloaded elevation grid by multiplying the two grids
grid_mask = grid * mask


fig = pygmt.Figure()
pygmt.makecpt(cmap="oleron", series=[-2000, 2000])

# Plot the elevation grid
fig.basemap(region=region, projection="M12c", frame=True)
fig.grdimage(grid=grid, cmap=True)
fig.basemap(frame="g1")
fig.plot(data=polygon, pen="2p,darkorange")

fig.shift_origin(xshift="+w+2c")

# Plot the masked elevation grid
fig.basemap(region=region, projection="M12c", frame=True)
fig.grdimage(grid=grid_mask, cmap=True)
fig.basemap(frame="g1")
fig.plot(data=polygon, pen="2p,darkorange")

fig.colorbar(frame=True)
fig.show()
