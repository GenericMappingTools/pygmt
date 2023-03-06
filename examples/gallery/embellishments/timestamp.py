"""
Timestamp
---------
The :meth:`pygmt.Figure.timestamp` method can draw the
GMT time stamp logo on the map/plot. A custom label
can be added via the ``label`` parameter. The timestamp
will always be shown in the bottom-left corner of the
figure.
"""

import pygmt

fig = pygmt.Figure()
fig.basemap(region=[20, 30, -10, 10], projection="X10c/5c")
fig.timestamp()
# Plot the GMT timestamp logo with a custom label.
fig.timestamp(label="Powered by PyGMT", justification="TL")
fig.show()
