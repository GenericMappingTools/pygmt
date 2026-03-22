"""
Plotting features on a 3-D surface
==================================

In addition to draping a dataset (grid or image) on top of a topographic surface,
you may want to add additional features like coastlines, symbols, and text
annotations. This tutorial shows how to use :meth:`pygmt.Figure.coast`,
:meth:`pygmt.Figure.plot3d`, and :meth:`pygmt.Figure.text` to add these features
on a 3-D surface created by :meth:`pygmt.Figure.grdview`.

This tutorial consists of three examples:

1. Adding coastlines on a 3-D surface
2. Adding symbols on a 3-D surface
3. Adding text annotations on a 3-D surface
"""

# %%

# Load the required packages
import pandas as pd
import pygmt

# %%
# 1. Adding coastlines on a 3-D surface
# -------------------------------------
#
# In the first example, we plot coastlines on top of a 3-D topographic surface.

# Load sample earth relief data for the region of Taiwan
# ------------------------------------------------------
#
# We use a region around Taiwan to demonstrate adding features on a 3-D surface.

# Define the study area in degrees East or North
region_2d = [119, 123, 21, 26]  # [lon_min, lon_max, lat_min, lat_max]

# Download elevation grid for the study region with a resolution of 5 arc-minutes.
# 5m provides clearer terrain than 10m while still being reasonably fast.
grd_relief = pygmt.datasets.load_earth_relief(resolution="05m", region=region_2d)

# Determine the 3-D region from the minimum and maximum values of the relief grid
region_3d = [*region_2d, grd_relief.min().to_numpy(), grd_relief.max().to_numpy()]

# Set up a colormap for topography and bathymetry
pygmt.makecpt(
    cmap="geo", series=[grd_relief.min().to_numpy(), grd_relief.max().to_numpy()]
)

# %%
# Create a 3-D surface and add coastlines
# ---------------------------------------
#
# First, we create a 3-D surface using :meth:`pygmt.Figure.grdview`. Then we add
# coastlines using :meth:`pygmt.Figure.coast` with a matching ``perspective`` setting.
# Here we set the z-level to 0 so coastlines are drawn at sea level.

fig = pygmt.Figure()

# Create a 3-D surface
fig.grdview(
    projection="M12c",  # Mercator projection with a width of 12 cm
    region=region_3d,
    grid=grd_relief,
    cmap=True,
    surftype="surface",
    shading="+a0/270+ne0.6",
    perspective=[157.5, 30],  # Azimuth and elevation for the 3-D plot
    zsize="1.5c",
    facade_fill="darkgray",
    frame=["xaf", "yaf", "WSnE"],
)

# Add coastlines on top of the 3-D surface
# Using perspective=True to inherit the viewing angle from grdview
fig.coast(
    perspective=[157.5, 30, 0],
    resolution="full",
    shorelines="1/1.5p,black",
)

# Add a colorbar
fig.colorbar(perspective=True, annot=1000, tick=500, label="Elevation", unit="m")

fig.show()

# %%
# 2. Adding symbols on a 3-D surface
# ----------------------------------
#
# In the second example, we add star symbols on top of the same 3-D surface. To plot
# symbols on a 3-D surface, use :meth:`pygmt.Figure.plot3d`. The z-coordinate should be
# set to a value at or above the maximum elevation to ensure the symbols are visible.

# Sample point data: five coastal cities around Taiwan
cities = pd.DataFrame(
    {
        "longitude": [
            121.74,
            121.61,
            121.14,
            120.30,
            120.53,
        ],  # Keelung, Hualien, Taitung, Kaohsiung, Taichung Port
        "latitude": [25.13, 23.99, 22.76, 22.63, 24.27],
        "name": ["Keelung", "Hualien", "Taitung", "Kaohsiung", "Taichung Port"],
    }
)

# Use one common z-level so all stars share the same shape and size.
z_stars = [grd_relief.max().to_numpy() + 1500] * len(cities.index)

fig = pygmt.Figure()

# Create a 3-D surface
fig.grdview(
    projection="M12c",
    region=region_3d,
    grid=grd_relief,
    cmap=True,
    surftype="surface",
    shading="+a0/270+ne0.6",
    perspective=[157.5, 30],
    zsize="1.5c",
    facade_fill="darkgray",
    frame=["xaf", "yaf", "WSnE"],
)

# Add coastlines
fig.coast(
    perspective=[157.5, 30, 0],
    resolution="f",
    shorelines="1/1.5p,black",
)

# Add five identical star symbols on top of the 3-D surface
fig.plot3d(
    x=cities.longitude,
    y=cities.latitude,
    z=z_stars,
    style="a0.65c",
    fill="gold",
    pen="0.8p,black",
    perspective=True,
    zsize="1.5c",  # Use the same zsize as grdview
    no_clip=True,
)

# Add a colorbar
fig.colorbar(perspective=True, annot=500, label="Elevation", unit="m")

fig.show()

# %%
# 3. Adding text annotations on a 3-D surface
# -------------------------------------------
#
# In the third example, we add text labels to the same 3-D figure. To add text
# annotations on a 3-D surface, use :meth:`pygmt.Figure.text` with
# ``perspective=True``. Note that the current implementation of ``text`` does not
# support a ``z`` parameter for controlling the vertical position of text labels.
# The text will be placed at the base of the 3-D plot (z=0).

fig = pygmt.Figure()

# Create a 3-D surface
fig.grdview(
    projection="M12c",
    region=region_3d,
    grid=grd_relief,
    cmap=True,
    surftype="surface",
    shading="+a0/270+ne0.6",
    perspective=[157.5, 30],
    zsize="1.5c",
    facade_fill="darkgray",
    frame=["xaf", "yaf", "WSnE"],
)

# Add coastlines
fig.coast(
    perspective=[157.5, 30, 0],
    resolution="full",
    shorelines="1/1.5p,black",
)

# Add symbols for cities
fig.plot3d(
    x=cities.longitude,
    y=cities.latitude,
    z=z_stars,
    style="a0.55c",
    fill="gold",
    pen="0.8p,black",
    perspective=True,
    zsize="1.5c",
    no_clip=True,
)

# Add text labels for cities
# Note: text is placed at z=0 (base level) since z parameter is not yet supported
fig.text(
    x=cities.longitude,
    y=cities.latitude,
    text=cities.name,
    perspective=True,
    font="11p,Helvetica-Bold,red",
    no_clip=True,  # Prevent text from being clipped at the frame boundaries
)

# Add a colorbar
fig.colorbar(perspective=True, annot=500, label="Elevation", unit="m")

fig.show()

# sphinx_gallery_thumbnail_number = 3
