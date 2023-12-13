"""
5. PyGMT I/O: Raster Inputs
===========================

In this tutorial, we'll explain how to pass raster data into PyGMT.

PyGMT supports two different ways to pass grids into PyGMT:

1. Directly pass the name of the raster file, with optional modifiers
2. Pass a :class:`xarray.DataArray` object
"""

# %%
import pygmt
import xarray as xr

# %%
# grid file name
# --------------
#
# Most PyGMT functions/methods that accept grid input data have a ``grid`` parameter.
# The easiest way to provide grid input data to PyGMT is by specifying the file name of
# the grid file (e.g., ``grid="mygrid.nc"``). This is useful when your grid is already
# stored in a file.

fig = pygmt.Figure()
fig.grdimage("@static_earth_relief.nc")
fig.show()

# %%
# :class:`xarray.DataArray`
# -------------------------
#
# The ``grid`` parameter also accepts a :class:`xarray.DataArray` object as input. This
# is useful when you want to work on grid that is already in memory.

import pygmt

grid = pygmt.datasets.load_earth_relief(resolution="01m", region=[-90, -70, 0, 20])
fig = pygmt.Figure()
fig.grdimage(grid)
fig.show()

import numpy as np

# Create a 2D grid of data
lon = np.linspace(-90, -70, 100)
lat = np.linspace(0, 20, 100)
data = np.sin(np.outer(lat, lon))

# Convert to xarray.DataArray
data_array = xr.DataArray(data, coords=[lat, lon], dims=["lat", "lon"])
print(data_array)

# %%
# In this tutorial, we've shown how to use netCDF files and xarray.DataArray objects with
# PyGMT. By leveraging the capabilities of xarray, you can easily integrate netCDF data
# into your PyGMT workflows for powerful geospatial data processing and visualization.
# Experiment with different PyGMT modules and create stunning visualizations for your data!
