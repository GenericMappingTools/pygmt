"""
Timestamp
---------
The :meth:`pygmt.Figure.timestamp` method can draw the
GMT timestamp logo on the figure. The timestamp
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
# Additionally, a custom label can be added via the ``label`` parameter. The
# label font can be defined via the ``font`` parameter and the timestamp string
# format via ``timefmt``.

fig = pygmt.Figure()
fig.coast(region="d", projection="H10c", land="black", water="cornsilk", frame="afg")
fig.timestamp(
    label="Powered by PyGMT",
    justification="TL",
    font="Times-Bold",
    timefmt="%Y-%m-%dT%H:%M",
)
fig.show()
