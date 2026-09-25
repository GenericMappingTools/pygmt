"""
Coastlines and borders
======================

Plotting coastlines and borders is handled by :meth:`pygmt.Figure.coast`.
"""

import pygmt

########################################################################################
# Shorelines
# ----------
#
# Use the ``shorelines`` argument to plot only the shorelines:

fig = pygmt.Figure()
fig.basemap(region="g", projection="W10i", frame=True)
fig.coast(shorelines=True)
fig.show()

########################################################################################
# The shorelines are divided in 4 levels:
#
# 1. coastline
# 2. lakeshore
# 3. island-in-lake shore
# 4. lake-in-island-in-lake shore
#
# You can specify which level you want to plot by passing the level number and a GMT pen
# configuration. For example, to plot just the coastlines with 0.5 thickness and black
# lines:

fig = pygmt.Figure()
fig.basemap(region="g", projection="W10i", frame=True)
fig.coast(shorelines="1/0.5p,black")
fig.show()

########################################################################################
# You can specify multiple levels (with their own pens) by passing a list to
# ``shorelines``:

fig = pygmt.Figure()
fig.basemap(region="g", projection="W10i", frame=True)
fig.coast(shorelines=["1/1p,black", "2/0.5p,red"])
fig.show()

########################################################################################
# Resolutions
# -----------
#
# The coastline database comes with 5 resolutions. The resolution drops by 80% between
# levels:
#
# 1. ``"c"``: crude
# 2. ``"l"``: low (default)
# 3. ``"i"``: intermediate
# 4. ``"h"``: high
# 5. ``"f"``: full

oahu = [-158.3, -157.6, 21.2, 21.8]
fig = pygmt.Figure()
for res in ["c", "l", "i", "h", "f"]:
    fig.coast(resolution=res, shorelines="1p", region=oahu, projection="M5i")
    fig.shift_origin(xshift="5i")
fig.show()

########################################################################################
# Land and water
# --------------
#
# Use the ``land`` and ``water`` attributes to specify a fill color for land and water
# bodies. The colors can be given by name or hex codes (like the ones used in HTML and
# CSS):

fig = pygmt.Figure()
fig.basemap(region="g", projection="W10i", frame=True)
fig.coast(land="#666666", water="skyblue")
fig.show()
