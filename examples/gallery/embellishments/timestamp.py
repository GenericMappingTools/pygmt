"""
Timestamp
---------
The :meth:`pygmt.Figure.timestamp` method can draw the
GMT timestamp logo on the map/plot. A custom label
can be added via the ``label`` parameter.
"""

import pygmt

fig = pygmt.Figure()
fig.timestamp()
fig.show()

# Plot the GMT timestamp logo with a custom label.
fig = pygmt.Figure()
fig.timestamp(label="Powered by PyGMT")
fig.show()
