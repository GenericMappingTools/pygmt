"""
Color land and water
--------------------

The ``land`` and ``water`` arguments of :meth:`pygmt.Figure.coast` specify a color to
fill in the land and water masses, respectively. You can use standard GMT color names or
give a hex value (like ``#333333``).
"""
import pygmt

fig = pygmt.Figure()
# Make a global Mollweide map with automatic ticks
fig.basemap(region="g", projection="W8i", frame=True)
# Plot the land as light gray
fig.coast(land="#666666", water="skyblue")
fig.show()
