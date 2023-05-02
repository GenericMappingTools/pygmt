r"""
Cross-section along a transect
==============================
:func:`pygmt.project` and :func:`pygmt.grdtrack` can be used to estimate
a quantity along a track.
In this example, the elevation is extracted from a gird provided via
:func:`pygmt.datasets.load_earth_relief`.

TODO

*This example is orientated on an example in the GMT/China documentation*:
https://docs.gmt-china.org/latest/examples/ex026/
"""

import pygmt

# Define region of study area
region_map = [122, 149, 30, 49]

# Create a new instance or object of the pygmt.Figure() class
fig = pygmt.Figure()

# ----------------------------------------------------------------------------
# Bottom: Map

fig.basemap(
    region=region_map,
    projection="M12c",  # Mercator projection with a width of 12 centimeters
    frame="af",
)

# Download grid for Earth relief with a resolution of 10 arc-minutes and
# gridline registration [Default]
grid_map = pygmt.datasets.load_earth_relief(
    resolution="10m",
    region=region_map,
)

# Plot the downloaded grid with color-coding for the elevation
fig.grdimage(grid=grid_map, cmap="oleron")

# Choose a track
fig.plot(
    x=[126, 146],  # Longitude in degrees East
    y=[42, 40],  # Latitude in degrees North
    # Draw a 2-points thick red dashed line for the track
    pen="2p,red,dashed",
)

# Add labels for start and end points of the track
fig.text(
    x=[126, 146],
    y=[42, 40],
    text=["A", "B"],
    offset="0c/0.2c",
    font="15p",
)

# Add a colorbar for the elevation
fig.colorbar(
    position="jBR+o0.7c/0.8c+h+w5c/0.3c+ml",
    box="+gwhite@30+p0.8p,black",
    frame=["x+lElevation", "y+lm"],
)

# ----------------------------------------------------------------------------
# Top: Track

# Shift plot origin 12.5 centimeters to the top
fig.shift_origin(yshift="12.5c")

fig.basemap(
    region=[0, 15, -8000, 6000],
    # Carthesian projection with a width of 12 centimeters and
    # a height of 3 centimeters
    projection="X12/3c",
    frame=["WSrt", "xa2f1+lDistance+u@.", "ya4000+lElevation / m"],
)

# Add labels for start and end points of the track
fig.text(
    x=[0, 15],
    y=[7000, 7000],
    text=["A", "B"],
    no_clip=True,  # Do not clip text that fall outside of the plot bounds
    font="10p",  # Use a font size of 10 points
)

# Set up track and store it in a DataFrame
track_df = pygmt.project(
    center="126/42",
    endpoint="146/40",
    generate="0.1",
)

# Download grid for Earth relief with a resolution of 4 arc-minutes and
# gridline registration [Default]
grid_track = pygmt.datasets.load_earth_relief(
    resolution="04m",
    region=region_map,
)

# Extract the elevation along the defined track from the downloaded grid
# and add it as new column "elevation" to the DataFrame
track_df = pygmt.grdtrack(
    grid=grid_track,
    points=track_df,
    newcolname="elevation",
)

# Plot water masses
fig.plot(
    x=[0, 15],
    y=[0, 0],
    fill="lightblue",  # Fill the polygon in "lightblue"
    # Draw a 0.25-points thick black solid outline
    pen="0.25p,black,solid",
    close="+y-8000",  # Force closed polygon
)

# Plot elevation along track
fig.plot(
    data=track_df,
    fill="gray",  # Fill the polygon in "gray"
    # Draw a 1-point thick black solid outline
    pen="1p,black,solid",
    close="+y-8000",  # Force closed polygon
    incols=[2, 3],  # Select order of input columns (zero-based indexing)
)

fig.show()
