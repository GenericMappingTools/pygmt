"""
Draping a dataset on top of a topographic surface
==================================================

It can be visually appealing to "drape" a dataset over a topographic surface. This can
be accomplished using the ``drape_grid`` parameter of :meth:`pygmt.Figure.grdview`.

This tutorial consists of two examples:

1. Draping a grid

2. Draping an image
"""

# %%

# Load the required packages
import pygmt
import rasterio
import xarray as xr

# %%
# 1. Drapping a grid
# ------------------
#
# In the first example, the seafloor crustal age is plotted with color-coding on top of
# the topographic map of an area of the Mid-Atlantic Ridge.

# Define the study area in degrees East or North
region_2d = [-50, 0, 36, 70]  # [lon_min, lon_max, lat_min, lat_max]

# Download elevation and crustal age grids for the study region with a resolution of 10
# arc-minutes and load them into xarray.DataArrays
grd_relief = pygmt.datasets.load_earth_relief(resolution="10m", region=region_2d)
grd_age = pygmt.datasets.load_earth_age(resolution="10m", region=region_2d)

# Determine the 3-D region from the minimum and maximum values of the relief grid
region_3d = [*region_2d, grd_relief.min().to_numpy(), grd_relief.max().to_numpy()]

# %%
# The topographic surface is created based on the grid passed to the ``grid`` parameter
# of :meth:`pygmt.Figure.grdview`; here we use a grid of the Earth relief. To add a
# color-coding based on *another* grid we have to pass a second grid to the
# ``drape_grid`` parameter; here we use a grid of the crustal age. In this case the
# colormap specified via the ``cmap`` parameter applies to the grid passed to
# ``drape_grid``, not to ``grid``. The azimuth and elevation of the 3-D plot are set via
# the ``perspective`` parameter.

fig = pygmt.Figure()

# Set up colormap for the crustal age
pygmt.config(COLOR_NAN="lightgray")
pygmt.makecpt(cmap="SCM/batlow", series=[0, 200, 1], reverse=True, overrule_bg=True)

fig.grdview(
    projection="M12c",  # Mercator projection with a width of 12 centimeters
    region=region_3d,
    grid=grd_relief,  # Use elevation grid for z values
    drape_grid=grd_age,  # Use crustal age grid for color-coding
    cmap=True,  # Use colormap created for the crustal age
    surftype="image",  # Create an image plot
    # Use an illumination from the azimuthal directions 0° (north) and 270°
    # (west) with a normalization via a cumulative Laplace distribution for
    # the shading
    shading="+a0/270+ne0.6",
    perspective=[157.5, 30],  # Azimuth and elevation for the 3-D plot
    zsize="1.5c",
    facade_fill="darkgray",
    frame=True,
)

# Add colorbar for the crustal age
fig.colorbar(frame=["x+lseafloor crustal age", "y+lMyr"], nan=True)

fig.show()


# %%
# 2. Draping an image
# -------------------
#
# In the second example, the flag of the European Union (EU) is plotted on top of a
# topographic map of northwest Europe. This example is modified from
# :gmt-docs:`GMT example 32 </gallery/ex32.html>`.
# We have to consider the dimension of the image we want to drap. The image we will
# download in this example has 1000 x 667 pixels, i.e. an aspect ratio of 3 x 2.

# Define the study area in degrees East or North, with an extend of 6 degrees for
# the longitude and 4 degrees for the latitude
region_2d = [3, 9, 50, 54]  # [lon_min, lon_max, lat_min, lat_max]

# Download elevation grid for the study region with a resolution of 30 arc-seconds and
# pixel registration and load it into an xarray.DataArray
grd_relief = pygmt.datasets.load_earth_relief(resolution="30s", region=region_2d)

# Determine the 3-D region from the minimum and maximum values of the relief grid
region_3d = [*region_2d, grd_relief.min().to_numpy(), grd_relief.max().to_numpy()]

# Download an PNG image of the flag of the EU using rasterio and load it into a
# xarray.DataArray
url_to_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Flag_of_Europe.svg/1024px-Flag_of_Europe.svg.png"
with rasterio.open(url_to_image) as dataset:
    data = dataset.read()
    drape_grid = xr.DataArray(data, dims=("band", "y", "x"))

# %%
# Again we create a 3-D plot with :meth:`pygmt.Figure.grdview` and pass an Earth relief
# grid to the ``grid`` parameter to create the topographic surface. But now we pass the
# PNG image which was loaded into an :class:`xarray.DataArray` to the ``drape_grid``
# parameter.

fig = pygmt.Figure()

# Set up a colormap with two colors for the EU flag: blue (0/51/153) for the background
# (value 0 in the netCDF file -> lower half of 0-255 range) and yellow (255/204/0) for
# the stars (value 255 -> upper half)
pygmt.makecpt(cmap="0/51/153,255/204/0", series=[0, 256, 128])

fig.grdview(
    projection="M12c",  # Mercator projection with a width of 12 centimeters
    region=region_3d,
    grid=grd_relief,  # Use elevation grid for z values
    drape_grid=drape_grid,  # Drape image grid for the EU flag on top
    cmap=True,  # Use colormap defined for the EU flag
    surftype="image",  # Create an image plot
    # Use an illumination from the azimuthal directions 0° (north) and 270° (west) with
    # a normalization via a cumulative Laplace distribution for the shading
    shading="+a0/270+ne0.6",
    perspective=[157.5, 30],  # Define azimuth, elevation for the 3-D plot
    zsize="1c",
    facade_fill="darkgray",
    frame=True,
)

fig.show()

# sphinx_gallery_thumbnail_number = 2
