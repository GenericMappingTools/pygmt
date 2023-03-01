"""
Calculating grid gradient with customized ``azimuth`` and ``normalize`` parameters
----------------------------------------------------------------------------------
The :func:`pygmt.grdgradient` function calculates the gradient of a grid file.
As input :func:`pygmt.grdgradient` gets a :class:`xarray.DataArray` object or
a path string to a grid file, calculates the respective gradient and returns
it as an :class:`xarray.DataArray` object. The ``azimuth`` parameter in order
to set the illumination light source direction. The ``normalize`` parameter
enhances the three-dimensional sense of the topography. It calculates the
azimuthal gradient of each point along a certain azimuth angle, then adjust
the brightness value of the color according to the positive/negative of the
azimuthal gradient and the amplitude of each point.
"""

import pygmt

# Define region of interest around Caucasus
region = [35, 50, 35, 45]

# Load sample grid (3 arc-minutes global relief) in target area
grid = pygmt.datasets.load_earth_relief(resolution="03m", region=region)

fig = pygmt.Figure()

# Define a colormap to be used for topography.
pygmt.makecpt(cmap="terra", series=[-7000, 7000])

# Define figure configuration
pygmt.config(FONT_TITLE="10p,5", MAP_TITLE_OFFSET="1p", MAP_FRAME_TYPE="plain")

# Setup subplot panels with three rows and four columns
with fig.subplot(
    nrows=3,
    ncols=4,
    figsize=("24c", "21c"),
    margins=["-1c", "-1c"],
    sharex="b",
    sharey="l",
):
    # e.g. 0/90 illuminates light source from the north (top) and east
    # (right), and so on.
    for azi in ["0/90", "0/180", "0/300"]:
        # `amp` (e.g. 2 or 10) controls the brightness value of the color
        # `e` and `t` are cumulative Laplace distribution and cumulative
        # Cauchy distribution, respectively.
        for nor in ["2t", "2e", "10t", "10e"]:
            # making an intensity DataArray using azimuth and normalize
            # parameters
            shade = pygmt.grdgradient(grid=grid, azimuth=azi, normalize=nor)
            fig.grdimage(
                grid=grid,
                shading=shade,
                projection="M5c",
                frame=["a4f2", f"+tazimuth={azi}, normalize={nor}"],
                cmap=True,
                panel=True,
            )

fig.show()
