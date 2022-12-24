"""
Sampling along tracks
---------------------

The :func:`pygmt.grdtrack` function samples a raster grid's value along
specified points. We will need to input a 2-D raster to ``grid`` which can be
an :class:`xarray.DataArray`. The argument passed to the ``points`` parameter
can be a :class:`pandas.DataFrame` table where the first two columns are
x and y (or longitude and latitude). Note also that there is a ``newcolname``
parameter that will be used to name the new column of values sampled from the
grid.

Alternatively, a NetCDF file path can be passed to ``grid``. An ASCII file path
can also be accepted for ``points``. To save an output ASCII file, a file name
argument needs to be passed to the ``outfile`` parameter.
"""
import os
import pygmt

# Load sample grid and point datasets
grid = pygmt.datasets.load_earth_relief()
points = pygmt.datasets.load_sample_data(name="ocean_ridge_points")
# Sample the bathymetry along the world's ocean ridges at specified track
# points
track = pygmt.grdtrack(points=points, grid=grid, newcolname="bathymetry")

# Set up colormap for Earth relief grid and save it in a file via the
# output parameter
pygmt.makecpt(
    cmap="gray",
    output="cpt_gray_relief.cpt",
    series=[int(grid.min()), int(grid.max()), 10],
)
# Set up colormap for data points of track and save it in a file via the
# output parameter
pygmt.makecpt(
    cmap="terra",
    output="cpt_terra_points.cpt",
    series="-1/1/0.01",  # for normalized values
)

fig = pygmt.Figure()
# Plot the Earth relief grid on Cylindrical Stereographic projection, masking
# land areas
fig.basemap(region="g", projection="Cyl_stere/150/-20/15c", frame=True)
fig.grdimage(grid=grid, cmap="cpt_gray_relief.cpt")
fig.coast(land="#666666")
# Plot the sampled bathymetry points using circles (c) with a diameter of
# 0.15 centimeters (c). Points are colored using elevation values (normalized
# for visual purposes)
fig.plot(
    x=track.longitude,
    y=track.latitude,
    style="c0.15c",
    cmap="cpt_terra_points.cpt",
    fill=(track.bathymetry - track.bathymetry.mean()) / track.bathymetry.std(),
)
# Add colorbar for Earth relief grid
fig.colorbar(
    cmap="cpt_gray_relief.cpt",
    position="JBC+o0c/1.2c+ml",  # placed at position Bottom Center
    frame=["af", "x+lelevation", "y+lm"],
)
# Add colorbar for data points of track
fig.colorbar(
    cmap="cpt_terra_points.cpt",
    position="JRM+ml",  # placed at position Right Middle
    frame=["a0.2f0.1", "+lnormalized elevation"],
)
fig.show()

# Cleanups (remove colormap files)
os.remove("cpt_gray_relief.cpt")
os.remove("cpt_terra_points.cpt")
