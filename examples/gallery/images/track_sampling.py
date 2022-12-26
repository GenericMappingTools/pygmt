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
import pygmt

# Load sample grid and point datasets
grid = pygmt.datasets.load_earth_relief()
points = pygmt.datasets.load_sample_data(name="ocean_ridge_points")
# Sample the bathymetry along the world's ocean ridges at specified track
# points
track = pygmt.grdtrack(points=points, grid=grid, newcolname="bathymetry")

fig = pygmt.Figure()
# Create a global map using a Cylindrical Stereographic projection
fig.basemap(region="g", projection="Cyl_stere/150/-20/15c", frame=True)

# Set up colormap for Earth relief grid
pygmt.makecpt(cmap="gray", series=[int(grid.min()), int(grid.max()), 10])
# Plot Earth relief grid with color-coding for the elevation
fig.grdimage(grid=grid, cmap=True)
# Add colorbar for Earth relief grid
fig.colorbar(
    cmap=True,
    position="JBC+o0c/1.2c+ml",  # Place colorbar at position Bottom Center
    frame=["af", "x+lelevation", "y+lm"],
)

# Mask land areas in gray and plote shorlines
fig.coast(land="#666666", shorelines="1/1p,black")

# Set up colormap for data points, which are normalized for visual purpose
pygmt.makecpt(cmap="terra", series=[-1, 1, 0.01])
# Plot the sampled bathymetry points using circles (c) with a diameter of
# 0.15 centimeters (c). Points are colored using normalized elevation values
fig.plot(
    x=track.longitude,
    y=track.latitude,
    style="c0.15c",
    cmap=True,
    fill=(track.bathymetry - track.bathymetry.mean()) / track.bathymetry.std(),
)
# Add colorbar for data points of track
fig.colorbar(
    cmap=True,
    position="JRM+ml",  # Place colorbar at position Right Middle
    frame=["a0.2f0.1", "+lnormalized elevation"],
)

fig.show()
