"""
Timestamp
---------
The :meth:`pygmt.Figure.timestamp` method can draw the
GMT timestamp logo on the figure. A custom label
can be added via the ``label`` parameter. The timestamp
will always be shown relative to the bottom-left corner
of the figure. By default, the ``offset`` and
``justification`` parameters are set to
``("-54p", "-54p")`` (x, y directions) and ``"BL"``
(bottom-left), respectively. 
"""

# sphinx_gallery_thumbnail_number = 1

import pygmt

fig = pygmt.Figure()
fig.basemap(region=[20, 30, -10, 10], projection="X10c/5c")
fig.timestamp()
fig.show()

###############################################################################
# Maybe some short description of the ``font`` and ``timefmt`` parameters.

fig = pygmt.Figure()
fig.coast(region="d", projection="H10c", land="black", water="cornsilk", frame="afg")
# Plot the GMT timestamp logo with a custom label.
fig.timestamp(label="Powered by PyGMT", justification="TL")
fig.show()
