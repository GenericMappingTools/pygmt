"""
3-D bar plot
============

TODO improve introduction

A 3-D bar plot of a grid can be created in two steps: (i) convert the grid into a table
via :func:`pygmt.grd2xyz` and (ii) plot this table as bars in 3-D using
:meth:`pygmt.Figure.plot3d`. The bars can be outlined, and the fill can be one color or
based on a quantity using a colormap.

We can create a 3-D bar plot for any collection of XYZ points, whether they lie on a
regular grid or are irregularly scattered. Therefore, it's clearer to start with a
general description of the 3-D bar plot itself and then mention that, as a special
case, we can convert a grid into XYZ and visualize it with the same routine.

The program plot3d allows us to plot three-dimensional symbols, including columnar plots.
As a simple demonstration, we will convert a gridded netCDF of bathymetry into an ASCII
xyz table and use the height information to draw a 2-D histogram in a 3-D perspective
view. We also use the height information to set to color of each column via a CPT file.
Our gridded bathymetry file is the 5 arc-minute global relief. Depth ranges from -5000
meter to sea-level. We produce the Figure by running this script.
"""

# %%
import pygmt
from pygmt.params import Position

# Define a study area around northern Japan with large elevation changes
region = [141, 147, 36, 43]

# Download a grid for the Earth relief with a resolution of 10 arc-minutes
grid = pygmt.datasets.load_earth_relief(resolution="10m", region=region)

# Convert the grid into a pandas DataFrame, with columns for longitude ("x"),
# latitude ("y") and elevation ("z")
grd_df = pygmt.grd2xyz(grid=grid)
zmin = grd_df["z"].min() - 50
zmax = grd_df["z"].max() + 50

# Add a fourth column "color" for the quantity used for the color-coding of the bars,
# here we use the elevation ("z")
grd_df["color"] = grd_df["z"]

# Create a 3-D bar plot with color-coding
fig = pygmt.Figure()

fig.basemap(
    region=[*region, zmin, zmax],
    projection="M10c",
    zsize="8c",
    frame=["WSneZ", "xaf", "yag", "za1000f500+lElevation / m"],
    perspective=(195, 30),
)

pygmt.makecpt(cmap="SCM/oleron", series=(zmin, zmax))
fig.plot3d(
    data=grd_df,
    # Use "o" to plot bars and give the desired size
    # The base of the bars is set via "+b"
    style=f"o0.34c+b{zmin}",
    cmap=True,
    pen="0.01p,gray30",
    perspective=True,
)
fig.colorbar(
    frame=["xa1000f500+lElevation", "y+lm"],
    position=Position("TR", cstype="inside", offset=1.4),
    orientation="vertical",
    length=7,
    move_text="label",
    label_as_column=True,
)

fig.show()
