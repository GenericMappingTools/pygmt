"""
Draping a data set on top of a topographic surface
==================================================

It can be visually appealing to "drape" a data set (grid or image) over a
topographic surface. This can be accomplished using the ``drapegrid`` parameter
of :meth:`pygmt.Figure.grdview`.

In the first example, the seafloor crustal age is plotted with color-coding
on top of the topographic map of an area of the Mid-Atlantic Ridge.

In the second example, the flag of Europe is plotted on top of a topographic
map of northwest Europe. This example is modified from GMT example 32 available
at https://docs.generic-mapping-tools.org/latest/gallery/ex32.html#example-32.
For the sake of simplicity the image grid is already stored as netCDF file
*@euflag.nc* in the GMT directory.

"""

# %%
import pygmt
import rasterio
import xarray as xr

# %%
# Grid of seafloor crustal age on top of topographic map of Mid-Atlantic Ridge
# -----------------------------------------------------------------------------

# Define study area
region_2d = [-50, 0, 36, 70]  # [lon_min, lon_max, lat_min, lat_max]
region_3d = [*region_2d, -5961, 3366.5]  # Append [z_min, z_max] to this list
perspective = [157.5, 30]  # Define azimuth, elevation for the 3-D plot

# -----------------------------------------------------------------------------
# Create new Figure instance
fig = pygmt.Figure()

# Download elevation and crustal age grids for the study region with a
# resolution of 3 arc-minutes and load them into xarray.DataArrays
grd_relief = pygmt.datasets.load_earth_relief(resolution="03m", region=region_2d)
grd_age = pygmt.datasets.load_earth_age(resolution="03m", region=region_2d)

# Set up colormap for curstal age
pygmt.config(COLOR_NAN="lightgray")
pygmt.makecpt(cmap="batlow", series=[0, 200, 1], reverse=True, overrule_bg=True)

fig.grdview(
    projection="M12c",  # Mercator projection with a width of 12 centimeters
    region=region_3d,
    grid=grd_relief,  # Use elevation grid for z values
    drapegrid=grd_age,  # Use crustal age grid for color-coding
    cmap=True,
    surftype="i",  # Create an image plot
    # Use an illumination from the azimuthal directions 0° (north) and 270°
    # (west) with a normalization via a cumulative Laplace distribution for
    # the shading
    shading="+a0/270+ne0.6",
    perspective=perspective,
    zsize="1.5c",
    plane="+gdarkgray",
    frame=True,
)

# -----------------------------------------------------------------------------
# Add colorbar for curstal age
fig.colorbar(frame=["x+lseafloor crustal age", "y+lMyr"], position="+n")

# Show figure
fig.show()


# %%
# Image of the flag of Europe on top of topographic map of northwest Europe
# -------------------------------------------------------------------------

# Define study area
region_2d = [3, 9, 50, 54]  # [lon_min, lon_max, lat_min, lat_max]
region_3d = [*region_2d, -10, 900]  # Append [z_min, z_max] to this list
perspective = [157.5, 30]  # Define azimuth, elevation for the 3-D plot

# Coordinates and names of cities
lons_cities = [7.10, 4.35, 5.69]  # degrees East
lats_cities = [50.73, 50.85, 50.85]  # degrees North
text_cities = ["Bonn", "Bruxelles", "Maastricht"]

# -----------------------------------------------------------------------------
# Create new Figure instance
fig = pygmt.Figure()

# Download elevation grid for the study region with a resolution of 30
# arc-seconds and pixel registration and load it into a xarray.DataArray
grd_relief = pygmt.datasets.load_earth_relief(resolution="30s", region=region_2d)

# Download a image of the flage of Europe using rasterio and load it into a
# xarray.DataArray
url_to_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Flag_of_Europe.svg/1000px-Flag_of_Europe.svg.png"
# url_to_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Flag_of_Germany.svg/1024px-Flag_of_Germany.svg.png"
with rasterio.open(url_to_image) as dataset:
    data = dataset.read()
    drapegrid = xr.DataArray(data, dims=("band", "y", "x"))

#%%
# Set up a colormap with two colors for the EU flag: blue (0/51/153) for the
# background (value 0 in the nedCDF file -> lower half of 0-255 range) and
# yellow (255/204/0) for the stars (value 255 -> upper half)
pygmt.makecpt(cmap="0/51/153,255/204/0", series=[0, 256, 128])  # [min, max[, step

fig.grdview(
    projection="M12c",  # Mercator projection with a width of 12 centimeters
    region=region_3d,
    grid=grd_relief,  # Use elevation grid for z values
    drapegrid=drapegrid,  # Drap image grid for the EU flag on top
    cmap=True,  # Use colormap defined for the EU flag
    surftype="i",  # Create an image plot
    # Use an illumination from the azimuthal directions 0° (north) and 270°
    # (west) with a normalization via a cumulative Laplace distribution for
    # the shading
    shading="+a0/270+ne0.6",
    perspective=perspective,
    zsize="1c",
    plane="+glightgray",
    frame=True,
)

# -----------------------------------------------------------------------------
# Plot water, broders, and shorelines on top
fig.coast(
    water="white@50",
    borders="1/1p,lightgray",
    shorelines="1/0.5p,gray30",
    perspective=perspective,
)

# -----------------------------------------------------------------------------
# Mark cities
# Plot markers
fig.plot(
    x=lons_cities,
    y=lats_cities,
    style="s0.3c",  # Use squares with a size of 0.3 centimeters
    pen="1.5p,white",
    fill="black",
    perspective=perspective,
)
# Add labels
fig.text(
    x=lons_cities,
    y=lats_cities,
    text=text_cities,
    justify="TL",  # Use Top Left corner as anchor point
    offset="0.3c/-0.3c",  # x / y directions, in centimeters
    font="12p",
    fill="white@30",  # Fill box in white with a transparency of 30 %
    perspective=perspective,
)

# -----------------------------------------------------------------------------
# Show figure
fig.show()

# sphinx_gallery_thumbnail_number = 1
