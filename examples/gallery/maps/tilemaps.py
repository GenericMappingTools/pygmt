"""
Tile maps
---------
The :meth:`pygmt.Figure.tilemap` method allows to plot
tiles from a tile server or local file as a basemap or overlay.
"""
import contextily
import pygmt

fig = pygmt.Figure()
fig.tilemap(
    region=[-157.84, -157.8, 21.255, 21.285],
    projection="M12c",
    # Set level of details (0-22)
    # Higher levels mean a zoom level closer to the Earth's
    # surface with more tiles covering a smaller
    # geographic area and thus more details and vice versa
    # Please note, not all zoom levels are always available
    zoom=14,
    # Use tiles from OpenStreetMap tile server
    source="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    frame="afg",
)

fig.show()

###############################################################################
# It's also possible to use tiles provided via the
# `contextily <https://github.com/geopandas/contextily>`__
# library. See :doc:`Contextily providers <contextily:providers_deepdive>`
# for a list of possible tilemap options.

fig = pygmt.Figure()
fig.tilemap(
    region=[-157.84, -157.8, 21.255, 21.285],
    projection="M12c",
    # Use the Stamen.Watercolor option from contextily
    source=contextily.providers.Stamen.Watercolor,
    frame="afg",
)

fig.show()
