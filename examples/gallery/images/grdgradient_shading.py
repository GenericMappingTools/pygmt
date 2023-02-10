"""
Calculating grid gradient, azimuth, and normalize
--------------------------------------
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

# Load sample grid (1 arc-minutes global relief) in target area
grid = pygmt.datasets.load_earth_relief(resolution="01m", region=region)

fig = pygmt.Figure()

# Define a colormap to be used for topography.
pygmt.makecpt(cmap="terra", series=[-7000, 7000])

# Define figure configuration
pygmt.config(FONT_TITLE="15p,5", MAP_TITLE_OFFSET="10p", MAP_FRAME_TYPE="plain")

# Setup subplots with 3x4 panels
with fig.subplot(nrows=3, ncols=4, figsize=("24c", "21c"), sharex="b", sharey="l", margins="-1c"):
    
    # e.g. 0/90 illuminates light source from the north (top) and east
    # (right), and so on.
    for i, azi in enumerate(["0/90", "0/180", "0/300"]):
        
        # `amp` controls the brightness value of the color
        # `e` and `t` are cumulative Laplace distribution and cumulative
        # Cauchy distribution, respectively.
        for j, nor in enumerate(["2t", "2e", "10t", "10e"]):
            index = i * 4 + j
            
            # making a intensity file with azimuth and normalize parameters
            shade = pygmt.grdgradient(grid=grid, azimuth=azi, normalize=nor)

            title = f"A={azi}, N={nor}"

            with fig.set_panel(panel=index):
                fig.grdimage(
                    grid=grid,
                    shading=shade,
                    projection="M5c",
                    frame=[f'+t"{title}"', "a4f2"],
                    cmap=True,
                )

fig.show()
