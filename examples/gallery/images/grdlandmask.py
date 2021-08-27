"""
Create 'wet-dry' mask grid
--------------------
The :meth:`pygmt.grdlandmash` method allows to set 
all nodes on land or water to a specified value using
the ``maskvalues`` parameter. 
"""

import pygmt

fig = pygmt.Figure()

# Assign a value of 0 for all water masses and a value of 1 for all land masses
grid = pygmt.grdlandmask(
    region=[-65, -40, -40, -20], spacing="5m", maskvalues="0/1", resolution="l"
)

# Plot clipped grid
fig.basemap(region=region, projection="M12c", frame=True)

fig.grdimage(grid=grid, cmap="lajolla")
fig.colorbar(position="JMR+o0.5c/0c+w8c")

fig.show()
