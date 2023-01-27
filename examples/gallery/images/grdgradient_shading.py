"""
Calculating grid gradient, azimuth and normalize
--------------------------------------
The :func:`pygmt.grdgradient` function calculates the gradient of a grid file.
In the example shown below we will see how to calculate a hillshade map based
on a Data Elevation Model (DEM). As input :func:`pygmt.grdgradient` gets
a :class:`xarray.DataArray` object or a path string to a grid file, calculates
the respective gradient and returns it as an :class:`xarray.DataArray` object.
We will use the ``azimuth`` and ``normalize`` parameters in order to set the illumination light source
directions and enhacing the three-dimensional effect of topography.
"""
import pygmt

# Define region of interest around Caucasus 
region = [35, 50, 35, 45]

# Load sample grid (1 arc-minutes global relief) in target area
grid = pygmt.datasets.load_earth_relief(resolution="01m", region=region)
cmap = pygmt.makecpt(cmap='terra', series=[-7000, 7000])

fig = pygmt.Figure()
# define figure configuration
pygmt.config(MAP_FRAME_TYPE="plain", 
            FONT_TITLE='15p,5',
            MAP_TITLE_OFFSET='5p',
            FONT_ANNOT_PRIMARY="8p")

with fig.subplot(nrows=3, ncols=4, figsize=("25c", "20c")):
    # azimuth: where is light source from. "0" means light source in the north 
    # direction. "0/180" means light source in the north and south directions.
    # "0/270" means light source in the north and west directions.
    for i, azi in enumerate(["0","0/180", "0/270"]):
        # normalize enhances the three-dimensional effect of topography. It is
        # more brighter(based on amplitude) to the light side. Conversely, it
        # is more darker to the dark side. "e" and "t" are differenct ways to
        # calculate gradient. 
        for j, nor in enumerate(["e0.5", "e2", "t0.5", "t2"]): 
            # index number starting from 0
            index = i * 4 + j 
            # Intensity file made from grdgradient
            shade = pygmt.grdgradient(grid=grid, azimuth=azi, normalize=nor)
            # Add a description of the parameter setting
            title = f'A={azi}, N={nor}'
            with fig.set_panel(panel=index):
                fig.grdimage(
                    grid=grid,
                    shading=shade,
                    projection="M5c",
                    frame=["a4f1",f'WSne+t"{title}"'],
                    cmap=cmap
                    )
# Add colorbar for gridded data          
fig.colorbar(cmap=cmap, 
             position='x8.5c/-1.1c+w7c/0.25c+h+mc',
             frame=["a2000f500", "x+lElevation", "y+lm"]
             )
fig.show()
