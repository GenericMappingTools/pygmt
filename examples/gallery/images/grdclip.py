"""
Clipping grid values
--------------------
The :meth:`pygmt.grdclip` method allows to clip defined ranges of grid values.
In the example shown below we set all elevation values (grid points) smaller
than 0 m (in general the bathymetric part of the grid) to a common value of
-2000 m via the ``below`` parameter.
"""

import pygmt

fig = pygmt.Figure()

# Define region of interest around the Hawaiian Islands
region = [-162, -153, 18, 23]

# Load sample grid (1 arc minute global relief) in target area
grid = pygmt.datasets.load_earth_relief(resolution="01m", region=region)

# Plot original grid
fig.basemap(region=region, projection="M12c", frame=["f", '+t"original grid"'])
fig.grdimage(grid=grid, cmap="oleron")

# Shift plot origin for second map -9 cm in y direction
fig.shift_origin(yshift="-9c")

# Set all grid points < 0 m to a value of -2000 m.
grid = pygmt.grdclip(grid, below=[0, -2000])

# Plot clipped grid
fig.basemap(region=region, projection="M12c", frame=["f", '+t"clipped grid"'])
fig.grdimage(grid=grid)
fig.colorbar(frame=["x+lElevation", "y+lm"])

fig.show()
