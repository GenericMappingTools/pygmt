"""
Create 'wet-dry' mask grid
--------------------------
The :func:`pygmt.grdlandmask` function allows setting
all nodes on land or water to a specified value using
the ``maskvalues`` parameter.
"""

import pygmt

fig = pygmt.Figure()

# Define region of interest
region = [-65, -40, -40, -20]

# Assign a value of 0 for all water masses and a value of 1 for all land
# masses.
# Use shoreline data with (l)ow resolution and set the grid spacing to
# 5 arc-minutes in x and y direction.
grid = pygmt.grdlandmask(region=region, spacing="5m", maskvalues=[0, 1], resolution="l")

# Plot clipped grid
fig.basemap(region=region, projection="M12c", frame=True)

# Define a colormap to be used for two categories, define the range of the
# new discrete CPT using series=(lowest_value, highest_value, interval),
# use color_model="+cwater,land" to write the discrete color palette
# "batlow" in categorical format and add water/land as annotations for the
# colorbar.
pygmt.makecpt(cmap="batlow", series=(0, 1, 1), color_model="+cwater,land")

fig.grdimage(grid=grid, cmap=True)
fig.colorbar(position="JMR+o0.5c/0c+w8c")

fig.show()
