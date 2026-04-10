"""
Create grid mask from polygons
==============================
:func:`pygmt.grdmask`.

:func:`pygmt.grdlandmask` and gallery example https://www.pygmt.org/latest/gallery/images/grdlandmask.html.
"""

# %%
import geopandas
import numpy as np
import pygmt
from shapely.geometry import Point

# %%
# Polygons based on NumPy arrays
# ------------------------------

# Define a study region
region = [125, 135, 25, 36]

# Define two closed polygons, here a quare and a triangle.
# Use nan to separate the polygons
polygon = np.array(
    [
        [129, 31],
        [134, 31],
        [134, 35],
        [129, 35],
        [129, 31],
        [np.nan, np.nan],
        [126, 26],
        [131, 26],
        [131, 30],
        [126, 26],
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


# %%
# US staat based on GeoPandas polygon geometry
# --------------------------------------------

region = [-126, -66, 25, 49]

provider = "https://naciscdn.org/naturalearth"
states = geopandas.read_file(
    f"{provider}/50m/cultural/ne_50m_admin_1_states_provinces.zip"
)
wyoming = states[states["name"] == "Missouri"]

grid = pygmt.datasets.load_earth_relief(region=region, resolution="01m")
mask = pygmt.grdmask(region=region, data=wyoming, spacing="01m", inside="NaN")
mask_lonlat = mask.rename(new_name_or_name_dict={"x": "lon", "y": "lat"})
grid_mask = grid * mask_lonlat


fig = pygmt.Figure()
pygmt.makecpt(cmap="oleron", series=[-2000, 2000])

# Plot the elevation grid
fig.basemap("L-96/35/33/41/12c", region=region, frame=True)
fig.grdimage(grid=grid, cmap=True)
fig.plot(data=wyoming, pen="1p,darkorange")

fig.shift_origin(xshift="+w+1c")

# Plot the masked elevation grid
fig.basemap("L-96/35/33/41/12c", region=region, frame=True)
fig.grdimage(grid=grid_mask, cmap=True)
fig.plot(data=wyoming, pen="1p,darkorange")

fig.colorbar(frame=True)
fig.show()


# %%
# Circle based on GeoPandas polygon geometry
# ------------------------------------------

region = [125, 135, 25, 36]

# Create a point and buffer it
point = geopandas.GeoSeries([Point(126.5, 33.5)])
circle = point.buffer(0.6)  # 10 is the radius

grid = pygmt.datasets.load_earth_relief(region=region, resolution="30s")
mask = pygmt.grdmask(region=region, data=circle, spacing="30s", outside="NaN")
mask_lonlat = mask.rename(new_name_or_name_dict={"x": "lon", "y": "lat"})
grid_mask = grid * mask_lonlat


fig = pygmt.Figure()
pygmt.makecpt(cmap="oleron", series=[-2000, 2000])

# Plot the elevation grid
fig.basemap(region=region, projection="M12c", frame=True)
fig.grdimage(grid=grid, cmap=True)
fig.plot(data=circle, pen="2p,darkorange")

fig.shift_origin(xshift="+w+2c")

# Plot the masked elevation grid
fig.basemap(region=region, projection="M12c", frame=True)
fig.grdimage(grid=grid_mask, cmap=True)
fig.plot(data=circle, pen="2p,darkorange")

fig.colorbar(frame=True)
fig.show()

# sphinx_gallery_thumbnail_number = 1
