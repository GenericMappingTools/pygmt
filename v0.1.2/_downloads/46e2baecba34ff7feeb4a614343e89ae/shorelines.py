"""
Shorelines
----------

Use :meth:`pygmt.Figure.coast` to display shorelines as black lines.
"""
import pygmt

fig = pygmt.Figure()
# Make a global Mollweide map with automatic ticks
fig.basemap(region="g", projection="W8i", frame=True)
# Display the shorelines as black lines with 0.5 point thickness
fig.coast(shorelines="0.5p,black")
fig.show()
